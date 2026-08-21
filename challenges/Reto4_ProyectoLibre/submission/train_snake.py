# -*- coding: utf-8 -*-
"""
Entrenamiento de Snake con Q-learning / DQN.

Permite activar y desactivar por separado cada uno de los ingredientes que le faltan al
código original, de modo que la comparación entre variantes sea controlada:

    --target-net    usa una red objetivo congelada (theta^-), sincronizada cada C pasos
    --detach        desconecta el objetivo TD del grafo de autograd
    --loss          mse (original) | huber (el del paper de DQN)
    --eps           fixed (original, 0.1) | decay (de 1.0 a 0.05)

Variantes usadas en el reto:

    baseline : diseño del autor tal cual (solo con el NameError corregido)
               python train_snake.py --variant baseline

    dqn      : baseline + red objetivo + detach  <- aísla exactamente el diagnóstico de §5
               python train_snake.py --variant dqn

Uso:
    python train_snake.py --variant baseline --episodes 1800 --out results/baseline.json
"""
import argparse, json, random, sys, time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

# El codigo del autor vive en snake_dqn/ y no se modifica
UPSTREAM_DIR = Path(__file__).resolve().parent / "snake_dqn"
sys.path.insert(0, str(UPSTREAM_DIR))
from model import QNetwork, get_network_input          # noqa: E402
from Game import GameEnvironment                        # noqa: E402
from replay_buffer import ReplayMemory                  # noqa: E402


# --------------------------------------------------------------------------- utilidades
def reset_clean(board):
    """resetgame() del autor + reinicio de la direccion y del contador de inanicion.

    El resetgame() original no restablece snake.dir ni time_since_apple, asi que cada
    partida heredaba la direccion de la anterior y arrancaba con el contador a medio correr.
    """
    board.resetgame()
    board.snake.dir = np.array([1., 0.])
    board.time_since_apple = 0


def reubicar_manzana_si_choca(board, max_intentos=100):
    """Corrige la 'manzana imposible': appleclass.eaten() reposiciona al azar sin comprobar
    si la casilla esta ocupada por el cuerpo de la serpiente.

    Cuando cae dentro del cuerpo la manzana es inalcanzable (para llegar habria que morderse),
    y la serpiente muere de inanicion con recompensa -1 por un fallo del ambiente, no suyo.
    La probabilidad crece con la longitud (~len/225), asi que castiga al agente justo cuando
    va ganando. Aqui la reubicamos hasta encontrar casilla libre.
    """
    cuerpo = {tuple(p) for p in board.snake.prevpos}
    for _ in range(max_intentos):
        if tuple(board.apple.pos) not in cuerpo:
            return False
        board.apple.pos = np.random.randint(1, board.gridsize, 2).astype("float")
    return True


@torch.no_grad()
def evaluate_greedy(net, num_games=30, seed=12345, max_steps=2000, fix_apple=False):
    """Evalua con epsilon = 0. Semilla propia y fija: todas las evaluaciones comparables entre si.

    Esta es la metrica honesta. El autor reporta el promedio de entrenamiento (con epsilon = 0.1),
    lo que subestima su agente en ~50% -- ver seccion 7 del notebook.
    """
    rng = np.random.RandomState(seed)
    state_np = np.random.get_state()
    np.random.seed(seed)                    # el ambiente usa np.random para las manzanas
    board = GameEnvironment(15, nothing=0, dead=-1, apple=1)
    lengths = []
    for _ in range(num_games):
        reset_clean(board)
        steps, length = 0, 0
        while not board.game_over and steps < max_steps:
            s = get_network_input(board.snake, board.apple)
            _, _, length = board.update_boardstate(int(torch.argmax(net(s))))
            if fix_apple:
                reubicar_manzana_si_choca(board)
            steps += 1
        lengths.append(length)
    np.random.set_state(state_np)           # no perturbar el RNG del entrenamiento
    return float(np.mean(lengths)), float(np.max(lengths))


def epsilon_at(episode, total, mode):
    """Programa de exploracion."""
    if mode == "fixed":
        return 0.1                                   # el valor fijo del autor
    start, end, frac = 1.0, 0.05, 0.6                # decae durante el 60% del entrenamiento
    t = min(1.0, episode / (frac * total))
    return start + t * (end - start)


# --------------------------------------------------------------------------- entrenamiento
def train(args):
    torch.set_num_threads(args.threads)
    random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)

    net = QNetwork(input_dim=10, hidden_dim=20, output_dim=5)
    opt = torch.optim.Adam(net.parameters(), lr=args.lr)

    target_net = None
    if args.target_net:
        target_net = QNetwork(input_dim=10, hidden_dim=20, output_dim=5)
        target_net.load_state_dict(net.state_dict())
        target_net.eval()

    board = GameEnvironment(15, nothing=0, dead=-1, apple=1)
    memory = ReplayMemory(args.buffer)
    reset_clean(board)

    hist = {k: [] for k in ("episode", "reward", "avg_len", "max_len", "loss",
                            "epsilon", "eval_avg_len", "eval_max_len")}
    grad_steps = 0
    t0 = time.time()

    for ep in range(1, args.episodes + 1):
        eps = epsilon_at(ep, args.episodes, args.eps)

        # ---- recoleccion: jugar N partidas guardando transiciones ----
        games, total_reward, lengths = 0, 0.0, []
        while games < args.games_per_episode:
            state = get_network_input(board.snake, board.apple)
            if np.random.uniform(0, 1) > eps:
                with torch.no_grad():
                    action = int(torch.argmax(net(state)))
            else:
                action = np.random.randint(0, 5)
            reward, done, len_of_snake = board.update_boardstate(action)
            if args.fix_apple:
                reubicar_manzana_si_choca(board)
            next_state = get_network_input(board.snake, board.apple)
            memory.push(state, action, reward, next_state, done)
            total_reward += reward
            if board.game_over:
                games += 1
                lengths.append(len_of_snake)
                reset_clean(board)

        # ---- aprendizaje ----
        ep_loss = 0.0
        for _ in range(args.updates):
            if len(memory) < args.batch:
                break
            opt.zero_grad()
            st, ac, rw, ns, dn = memory.sample(args.batch)
            st = torch.cat([x.unsqueeze(0) for x in st], dim=0)
            ns = torch.cat([x.unsqueeze(0) for x in ns], dim=0)
            ac = torch.LongTensor(ac); rw = torch.FloatTensor(rw); dn = torch.FloatTensor(dn)

            q_sa = net(st).gather(1, ac.unsqueeze(1)).squeeze(1)

            # --- el objetivo TD: aqui esta toda la diferencia entre las variantes ---
            bootstrap_net = target_net if args.target_net else net
            if args.detach:
                with torch.no_grad():
                    q_next = torch.max(bootstrap_net(ns), 1)[0]
            else:
                q_next = torch.max(bootstrap_net(ns), 1)[0]     # sigue enganchado al grafo
            target = rw + args.gamma * q_next * (1 - dn)

            loss = F.smooth_l1_loss(q_sa, target) if args.loss == "huber" else F.mse_loss(q_sa, target)
            loss.backward(); opt.step()
            ep_loss += loss.item()
            grad_steps += 1

            if args.target_net and grad_steps % args.sync_every == 0:
                target_net.load_state_dict(net.state_dict())

        memory.truncate()

        # ---- registro ----
        hist["episode"].append(ep)
        hist["reward"].append(total_reward)
        hist["avg_len"].append(float(np.mean(lengths)))
        hist["max_len"].append(float(np.max(lengths)))
        hist["loss"].append(ep_loss)
        hist["epsilon"].append(eps)

        if ep % args.eval_every == 0 or ep == args.episodes:
            g_avg, g_max = evaluate_greedy(net, num_games=args.eval_games, fix_apple=args.fix_apple)
            hist["eval_avg_len"].append([ep, g_avg])
            hist["eval_max_len"].append([ep, g_max])
            el = time.time() - t0
            eta = el / ep * (args.episodes - ep)
            print(f"[{args.variant}] ep {ep:5}/{args.episodes}  eps={eps:.3f}  "
                  f"train_len={np.mean(lengths):5.2f}  GREEDY_len={g_avg:5.2f} (max {g_max:3.0f})  "
                  f"loss={ep_loss:8.2f}  transcurrido={el/60:5.1f}m  faltan={eta/60:5.1f}m",
                  flush=True)

        # ---- tope de reloj ----
        # A medida que el agente mejora, sus partidas duran mas pasos y cada episodio se
        # encarece. Sin este tope, el tiempo total es impredecible. Cortar por reloj mantiene
        # ademas la comparacion justa: ambas variantes reciben el MISMO presupuesto de tiempo.
        if args.max_minutes and (time.time() - t0) / 60 >= args.max_minutes:
            print(f"\n[{args.variant}] tope de {args.max_minutes} min alcanzado en el episodio {ep} "
                  f"(de {args.episodes} previstos) -- guardando y terminando.", flush=True)
            args.episodes_completed = ep
            break

    # ---- guardar ----
    out = Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    final_avg, final_max = evaluate_greedy(net, num_games=200, fix_apple=args.fix_apple)
    payload = {
        "variant": args.variant,
        "config": {k: v for k, v in vars(args).items() if k != "out"},
        "history": hist,
        "final_greedy": {"avg_len": final_avg, "max_len": final_max, "num_games": 200},
        "wall_clock_s": time.time() - t0,
        "grad_steps": grad_steps,
        "episodes_completed": len(hist["episode"]),
        "episodes_requested": args.episodes,
    }
    out.write_text(json.dumps(payload, indent=1), encoding="utf-8")
    torch.save(net.state_dict(), out.with_suffix(".pt"))
    print(f"\n[{args.variant}] LISTO en {(time.time()-t0)/60:.1f} min")
    print(f"[{args.variant}] greedy final sobre 200 partidas: media={final_avg:.2f}  max={final_max:.0f}")
    print(f"[{args.variant}] guardado en {out} y {out.with_suffix('.pt')}")


# --------------------------------------------------------------------------- CLI
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--variant", default="custom", help="baseline | dqn | custom")
    p.add_argument("--episodes", type=int, default=1800)
    p.add_argument("--games-per-episode", type=int, default=30)
    p.add_argument("--updates", type=int, default=500)
    p.add_argument("--batch", type=int, default=20)
    p.add_argument("--buffer", type=int, default=1000)
    p.add_argument("--lr", type=float, default=1e-4)
    p.add_argument("--gamma", type=float, default=0.99)
    p.add_argument("--sync-every", type=int, default=500, help="pasos de gradiente entre sincronizaciones")
    p.add_argument("--eval-every", type=int, default=100)
    p.add_argument("--eval-games", type=int, default=30)
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--threads", type=int, default=1)
    p.add_argument("--fix-apple", dest="fix_apple", action="store_true",
                   help="corrige la manzana imposible: no la coloca sobre el cuerpo")
    p.add_argument("--max-minutes", type=float, default=None,
                   help="tope de reloj: corta el entrenamiento y guarda al alcanzarlo")
    p.add_argument("--out", default=None)

    g = p.add_mutually_exclusive_group(); g.add_argument("--target-net", dest="target_net", action="store_true")
    g.add_argument("--no-target-net", dest="target_net", action="store_false")
    g2 = p.add_mutually_exclusive_group(); g2.add_argument("--detach", dest="detach", action="store_true")
    g2.add_argument("--no-detach", dest="detach", action="store_false")
    p.add_argument("--loss", choices=["mse", "huber"], default=None)
    p.add_argument("--eps", choices=["fixed", "decay"], default=None)
    p.set_defaults(target_net=None, detach=None)

    args = p.parse_args()

    # Presets. baseline = el diseño del autor; dqn = baseline + red objetivo + detach.
    presets = {
        "baseline": dict(target_net=False, detach=False, loss="mse", eps="fixed"),
        "dqn":      dict(target_net=True,  detach=True,  loss="mse", eps="fixed"),
    }
    if args.variant in presets:
        for k, v in presets[args.variant].items():
            if getattr(args, k) is None:
                setattr(args, k, v)
    for k, v in dict(target_net=False, detach=False, loss="mse", eps="fixed").items():
        if getattr(args, k) is None:
            setattr(args, k, v)
    if args.out is None:
        args.out = f"results/{args.variant}.json"

    print(f"=== variante '{args.variant}' ===")
    print(f"  red objetivo : {args.target_net}" + (f"  (sync cada {args.sync_every} pasos)" if args.target_net else ""))
    print(f"  detach       : {args.detach}")
    print(f"  perdida      : {args.loss}")
    print(f"  epsilon      : {args.eps}")
    print(f"  manzana      : {'corregida' if args.fix_apple else 'original (puede caer sobre el cuerpo)'}")
    print(f"  episodios    : {args.episodes}  x {args.games_per_episode} partidas  x {args.updates} updates")
    print(f"  hilos torch  : {args.threads}\n")
    train(args)


if __name__ == "__main__":
    main()
