"""Carga de resultados y gráficas para el análisis del Reto 4."""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

RESULTS = Path("results")

# Paleta consistente en todo el notebook
C_BASE = "#f0883e"  # sin red objetivo
C_DQN = "#58a6ff"  # con red objetivo
C_AUTOR = "#7ee787"
C_AZAR = "#8b949e"
C_GRID = "#d0d7de"


def cargar(nombre):
    """Carga un resultado de entrenamiento por nombre de archivo (sin .json)."""
    p = RESULTS / f"{nombre}.json"
    if not p.exists():
        raise FileNotFoundError(f"No existe {p}. ¿Ya corrió el entrenamiento?")
    return json.loads(p.read_text(encoding="utf-8"))


def cargar_factorial(carpeta="multi"):
    """Carga todas las corridas del factorial. Devuelve lista de dicts con metadatos."""
    out = []
    for p in sorted((RESULTS / carpeta).glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        variante, manzana, semilla = p.stem.rsplit("_", 2)
        d["_variante"] = variante
        d["_manzana"] = manzana
        d["_semilla"] = int(semilla.lstrip("s"))
        d["_celda"] = f"{variante}/{manzana}"
        out.append(d)
    return out


def serie_greedy(res):
    """Devuelve (episodios, longitud greedy) de las evaluaciones periódicas."""
    ev = np.array(res["history"]["eval_avg_len"], dtype=float)
    return ev[:, 0], ev[:, 1]


def _suavizar(y, k=15):
    if len(y) < k:
        return np.asarray(y, dtype=float)
    return np.convolve(y, np.ones(k) / k, mode="valid")


def curvas_largas(base, dqn, figsize=(13, 4.2)):
    """Compara las dos corridas largas: entrenamiento, evaluación greedy y pérdida."""
    fig, axes = plt.subplots(1, 3, figsize=figsize)

    # --- 1. longitud durante el entrenamiento (con epsilon = 0.1) ---
    ax = axes[0]
    for res, color, etq in [
        (base, C_BASE, "sin red objetivo"),
        (dqn, C_DQN, "con red objetivo"),
    ]:
        y = res["history"]["avg_len"]
        ax.plot(y, color=color, alpha=0.18, lw=0.8)
        s = _suavizar(y)
        ax.plot(np.arange(len(s)) + 15 // 2, s, color=color, lw=1.8, label=etq)
    ax.set_title("Entrenamiento (ε = 0,1)", fontsize=10)
    ax.set_xlabel("episodio")
    ax.set_ylabel("longitud media")

    # --- 2. evaluación greedy (la métrica honesta) ---
    ax = axes[1]
    for res, color, etq in [
        (base, C_BASE, "sin red objetivo"),
        (dqn, C_DQN, "con red objetivo"),
    ]:
        x, y = serie_greedy(res)
        ax.plot(x, y, color=color, lw=1.6, marker="o", ms=2.5, label=etq)
    ax.set_title("Evaluación greedy (ε = 0)", fontsize=10)
    ax.set_xlabel("episodio")
    ax.set_ylabel("longitud media")

    # --- 3. pérdida ---
    ax = axes[2]
    for res, color, etq in [
        (base, C_BASE, "sin red objetivo"),
        (dqn, C_DQN, "con red objetivo"),
    ]:
        y = res["history"]["loss"]
        ax.plot(y, color=color, alpha=0.20, lw=0.8)
        s = _suavizar(y)
        ax.plot(np.arange(len(s)) + 15 // 2, s, color=color, lw=1.8, label=etq)
    ax.set_yscale("log")
    ax.set_title("Pérdida TD (escala log)", fontsize=10)
    ax.set_xlabel("episodio")
    ax.set_ylabel("pérdida acumulada")

    for ax in axes:
        ax.grid(alpha=0.25, ls=":")
        ax.legend(fontsize=8, frameon=False)
        for s_ in ax.spines.values():
            s_.set_alpha(0.3)
    fig.tight_layout()
    return fig


def brecha_train_greedy(res, titulo, ax=None):
    """Dibuja la brecha entre la métrica de entrenamiento (ε=0,1) y la greedy (ε=0).

    Es el hallazgo de §7 aplicado a nuestros propios datos.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(6, 4))
    x, g = serie_greedy(res)
    tr = np.array(res["history"]["avg_len"], dtype=float)
    tr_en_x = np.array([tr[max(0, int(e) - 1)] for e in x])

    ax.plot(
        x,
        tr_en_x,
        color=C_BASE,
        lw=1.6,
        marker="s",
        ms=3,
        label="entrenamiento (ε = 0,1)",
    )
    ax.plot(x, g, color=C_DQN, lw=1.6, marker="o", ms=3, label="greedy (ε = 0)")
    ax.fill_between(x, tr_en_x, g, color=C_DQN, alpha=0.12)
    ax.set_title(titulo, fontsize=10)
    ax.set_xlabel("episodio")
    ax.set_ylabel("longitud media")
    ax.grid(alpha=0.25, ls=":")
    ax.legend(fontsize=8, frameon=False)
    return ax


def tabla_factorial(corridas):
    """Resume el factorial: media y dispersión del desempeño final por celda."""
    celdas = {}
    for r in corridas:
        celdas.setdefault(r["_celda"], []).append(r["final_greedy"]["avg_len"])
    filas = []
    for celda, vals in sorted(celdas.items()):
        v = np.array(vals)
        variante, manzana = celda.split("/")
        filas.append(
            {
                "celda": celda,
                "red objetivo": "sí" if variante == "dqn" else "no",
                "manzana": "corregida" if manzana == "fix" else "original",
                "n": len(v),
                "media": v.mean(),
                "desv": v.std(ddof=1) if len(v) > 1 else 0.0,
                "min": v.min(),
                "max": v.max(),
                "valores": sorted(v.round(2).tolist()),
            }
        )
    return filas


def grafico_factorial(corridas, figsize=(11, 4.2)):
    """Dos vistas del factorial: dispersión por celda y efecto de cada factor."""
    fig, axes = plt.subplots(1, 2, figsize=figsize)

    orden = ["baseline/orig", "dqn/orig", "baseline/fix", "dqn/fix"]
    etiquetas = [
        "sin θ⁻\nmanzana orig.",
        "con θ⁻\nmanzana orig.",
        "sin θ⁻\nmanzana corr.",
        "con θ⁻\nmanzana corr.",
    ]
    porcelda = {}
    for r in corridas:
        porcelda.setdefault(r["_celda"], []).append(r["final_greedy"]["avg_len"])

    # --- 1. cada semilla como un punto ---
    ax = axes[0]
    for i, celda in enumerate(orden):
        vals = porcelda.get(celda, [])
        if not vals:
            continue
        color = C_DQN if celda.startswith("dqn") else C_BASE
        x = np.random.RandomState(i).normal(i, 0.055, len(vals))
        ax.scatter(
            x,
            vals,
            color=color,
            s=45,
            alpha=0.85,
            zorder=3,
            edgecolor="white",
            linewidth=0.6,
        )
        m = np.mean(vals)
        ax.plot([i - 0.24, i + 0.24], [m, m], color=color, lw=2.4, zorder=4)
        if len(vals) > 1:
            sd = np.std(vals, ddof=1)
            ax.plot([i, i], [m - sd, m + sd], color=color, lw=1.2, alpha=0.6, zorder=2)
    ax.set_xticks(range(len(orden)))
    ax.set_xticklabels(etiquetas, fontsize=8)
    ax.set_ylabel("longitud greedy final")
    ax.set_title("Cada punto es una semilla\n(barra = media ± 1 desv.)", fontsize=10)

    # --- 2. efecto marginal de cada factor ---
    ax = axes[1]

    def marg(pred):
        v = [r["final_greedy"]["avg_len"] for r in corridas if pred(r)]
        return np.mean(v), (np.std(v, ddof=1) / np.sqrt(len(v)) if len(v) > 1 else 0)

    grupos = [
        ("sin red obj.", lambda r: r["_variante"] == "baseline", C_BASE),
        ("con red obj.", lambda r: r["_variante"] == "dqn", C_DQN),
        ("manzana orig.", lambda r: r["_manzana"] == "orig", "#a371f7"),
        ("manzana corr.", lambda r: r["_manzana"] == "fix", "#d2a8ff"),
    ]
    for i, (_etq, pred, color) in enumerate(grupos):
        m, se = marg(pred)
        ax.bar(
            i,
            m,
            yerr=se,
            color=color,
            alpha=0.85,
            capsize=4,
            error_kw=dict(lw=1.2, alpha=0.7),
        )
    ax.set_xticks(range(len(grupos)))
    ax.set_xticklabels([g[0] for g in grupos], fontsize=8)
    ax.set_ylabel("longitud greedy final")
    ax.set_title(
        "Efecto marginal de cada factor\n(barra de error = error estándar)", fontsize=10
    )

    for ax in axes:
        ax.grid(alpha=0.25, ls=":", axis="y")
        for s_ in ax.spines.values():
            s_.set_alpha(0.3)
    fig.tight_layout()
    return fig
