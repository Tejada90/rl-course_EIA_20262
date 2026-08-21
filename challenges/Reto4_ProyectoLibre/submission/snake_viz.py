# -*- coding: utf-8 -*-
"""
Visualización del agente jugando Snake, embebible en el notebook y en el HTML exportado.

A diferencia del WatchAgent.ipynb del autor (que abre una ventana de Pygame y necesita que
alguien presione ESC para parar), esto:
  - no requiere pantalla ni Pygame,
  - juega un numero fijo de partidas y termina solo,
  - produce un reproductor HTML+JS autocontenido que sobrevive a la exportacion del notebook.
"""
import numpy as np
import torch
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation

GRID = 15


def record_game(net, gridsize=GRID, seed=7, max_steps=400, epsilon=0.0):
    """Juega una partida greedy y devuelve la lista de fotogramas.

    Cada fotograma es un dict con el cuerpo de la serpiente, la manzana y los marcadores.
    """
    from Game import GameEnvironment
    from model import get_network_input

    np.random.seed(seed)
    torch.manual_seed(seed)
    board = GameEnvironment(gridsize, nothing=0, dead=-1, apple=1)
    board.resetgame()
    board.snake.dir = np.array([1., 0.])
    board.time_since_apple = 0

    frames = []
    for step in range(max_steps):
        frames.append({
            "body": [p.copy() for p in board.snake.prevpos],
            "head": board.snake.pos.copy(),
            "apple": board.apple.pos.copy(),
            "score": board.apple.score,
            "length": len(board.snake),
            "step": step,
        })
        state = get_network_input(board.snake, board.apple)
        if epsilon > 0 and np.random.uniform(0, 1) < epsilon:
            action = np.random.randint(0, 5)
        else:
            with torch.no_grad():
                action = int(torch.argmax(net(state)))
        board.update_boardstate(action)
        if board.game_over:
            frames.append({**frames[-1], "dead": True})
            break
    return frames


def animate(frames, gridsize=GRID, titulo="Agente", intervalo=90, figsize=(4.2, 4.6)):
    """Convierte los fotogramas en un reproductor HTML+JS autocontenido."""
    fig, ax = plt.subplots(figsize=figsize, dpi=80)
    fig.patch.set_facecolor("#0d1117")
    ax.set_facecolor("#0d1117")

    ax.set_xlim(-0.5, gridsize - 0.5)
    ax.set_ylim(gridsize - 0.5, -0.5)          # y invertido: fila 0 arriba
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_aspect("equal")
    for lado in ax.spines.values():
        lado.set_color("#30363d")

    titulo_txt = ax.set_title("", color="#e6edf3", fontsize=10, pad=8)
    patches = []

    def dibujar(i):
        nonlocal patches
        for p in patches:
            p.remove()
        patches = []
        f = frames[i]

        cuerpo = f["body"]
        n = len(cuerpo)
        for j, pos in enumerate(cuerpo):
            # degradado: la cola mas oscura que la cabeza
            t = (j + 1) / max(n, 1)
            color = (0.15 + 0.35 * t, 0.55 + 0.40 * t, 0.30 + 0.25 * t)
            r = mpatches.Rectangle((pos[0] - 0.5, pos[1] - 0.5), 1, 1,
                                   facecolor=color, edgecolor="#0d1117", linewidth=0.5)
            ax.add_patch(r); patches.append(r)

        cab = f["head"]
        r = mpatches.Rectangle((cab[0] - 0.5, cab[1] - 0.5), 1, 1,
                               facecolor="#ffd33d" if f.get("dead") else "#7ee787",
                               edgecolor="#0d1117", linewidth=0.8)
        ax.add_patch(r); patches.append(r)

        ap = f["apple"]
        c = mpatches.Circle((ap[0], ap[1]), 0.38, facecolor="#f85149", edgecolor="none")
        ax.add_patch(c); patches.append(c)

        estado = "  ✗ murió" if f.get("dead") else ""
        titulo_txt.set_text(f"{titulo}   long: {f['length']}   manzanas: {f['score']}{estado}")
        return patches + [titulo_txt]

    anim = animation.FuncAnimation(fig, dibujar, frames=len(frames),
                                   interval=intervalo, blit=False)
    plt.close(fig)
    return anim


def jugar_y_animar(net, titulo="Agente", seed=7, max_steps=400, gridsize=GRID):
    """Atajo: graba una partida y devuelve el reproductor HTML listo para mostrar."""
    from IPython.display import HTML
    frames = record_game(net, gridsize=gridsize, seed=seed, max_steps=max_steps)
    return HTML(animate(frames, gridsize=gridsize, titulo=titulo).to_jshtml(default_mode="once"))


def animate_comparison(agentes, gridsize=GRID, seed=7, max_steps=400,
                       intervalo=90, alto=3.6, dpi=62):
    """Anima varios agentes en paralelo dentro de un solo reproductor.

    `agentes` es un dict {titulo: red}. Todos juegan con la MISMA semilla, asi que
    reciben la misma secuencia de manzanas y las diferencias son atribuibles a la politica.

    Las partidas duran distinto; las mas cortas se congelan en su ultimo fotograma para
    que la animacion siga mostrando el marcador final de cada agente.
    """
    grabaciones = {t: record_game(n, gridsize=gridsize, seed=seed, max_steps=max_steps)
                   for t, n in agentes.items()}
    n_frames = max(len(f) for f in grabaciones.values())
    for t, f in grabaciones.items():                       # congelar las partidas cortas
        if len(f) < n_frames:
            f.extend([{**f[-1], "dead": True}] * (n_frames - len(f)))

    k = len(agentes)
    fig, axes = plt.subplots(1, k, figsize=(alto * k, alto + 0.9), dpi=dpi)
    if k == 1:
        axes = [axes]
    fig.patch.set_facecolor("#0d1117")

    titulos = []
    for ax in axes:
        ax.set_facecolor("#0d1117")
        ax.set_xlim(-0.5, gridsize - 0.5)
        ax.set_ylim(gridsize - 0.5, -0.5)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_aspect("equal")
        for lado in ax.spines.values():
            lado.set_color("#30363d")
        titulos.append(ax.set_title("", color="#e6edf3", fontsize=9, pad=6))

    estado = {"patches": [[] for _ in range(k)]}

    def dibujar(i):
        artistas = []
        for idx, (titulo, frames) in enumerate(grabaciones.items()):
            ax = axes[idx]
            for p in estado["patches"][idx]:
                p.remove()
            estado["patches"][idx] = []
            f = frames[i]

            cuerpo = f["body"]; n = len(cuerpo)
            for j, pos in enumerate(cuerpo):
                t = (j + 1) / max(n, 1)
                color = (0.15 + 0.35 * t, 0.55 + 0.40 * t, 0.30 + 0.25 * t)
                r = mpatches.Rectangle((pos[0] - 0.5, pos[1] - 0.5), 1, 1,
                                       facecolor=color, edgecolor="#0d1117", linewidth=0.4)
                ax.add_patch(r); estado["patches"][idx].append(r)

            cab = f["head"]
            r = mpatches.Rectangle((cab[0] - 0.5, cab[1] - 0.5), 1, 1,
                                   facecolor="#ffd33d" if f.get("dead") else "#7ee787",
                                   edgecolor="#0d1117", linewidth=0.7)
            ax.add_patch(r); estado["patches"][idx].append(r)

            ap = f["apple"]
            c = mpatches.Circle((ap[0], ap[1]), 0.38, facecolor="#f85149", edgecolor="none")
            ax.add_patch(c); estado["patches"][idx].append(c)

            marca = " ✗" if f.get("dead") else ""
            titulos[idx].set_text(f"{titulo}\nlong {f['length']}  manzanas {f['score']}{marca}")
            artistas += estado["patches"][idx] + [titulos[idx]]
        return artistas

    # Los titulos ocupan dos lineas; dejamos margen superior para que no se recorten.
    fig.subplots_adjust(top=0.82, bottom=0.03, left=0.02, right=0.98, wspace=0.08)
    anim = animation.FuncAnimation(fig, dibujar, frames=n_frames, interval=intervalo, blit=False)
    plt.close(fig)
    return anim
