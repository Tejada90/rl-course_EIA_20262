"""Métricas comunes para comparar algoritmos de bandits."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _as_non_empty_vector(values: ArrayLike, name: str) -> NDArray[np.float64]:
    result = np.asarray(values, dtype=np.float64)
    if result.ndim != 1 or result.size == 0:
        raise ValueError(f"{name} debe ser un arreglo unidimensional no vacío.")
    if not np.all(np.isfinite(result)):
        raise ValueError(f"{name} solo puede contener valores finitos.")
    return result


def _as_actions(actions: ArrayLike) -> NDArray[np.int64]:
    raw = np.asarray(actions)
    if raw.ndim != 1 or raw.size == 0:
        raise ValueError("actions debe ser un arreglo unidimensional no vacío.")
    if not np.issubdtype(raw.dtype, np.integer):
        raise TypeError("actions solo puede contener índices enteros.")
    return raw.astype(np.int64, copy=False)


def cumulative_average(rewards: ArrayLike) -> NDArray[np.float64]:
    """Calcula la recompensa media acumulada en cada paso."""

    values = _as_non_empty_vector(rewards, "rewards")
    counts = np.arange(1, values.size + 1, dtype=np.float64)
    return np.cumsum(values) / counts


def cumulative_regret(
    actions: ArrayLike,
    true_means: ArrayLike,
) -> NDArray[np.float64]:
    """Calcula el pseudo-regret acumulado respecto al brazo óptimo."""

    selected = _as_actions(actions)
    means = _as_non_empty_vector(true_means, "true_means")
    if np.any(selected < 0) or np.any(selected >= means.size):
        raise ValueError("actions contiene un índice de brazo inválido.")
    instantaneous = np.max(means) - means[selected]
    return np.cumsum(instantaneous)


def optimal_action_rate(
    actions: ArrayLike,
    optimal_arm: int,
) -> NDArray[np.float64]:
    """Calcula el porcentaje acumulado de selecciones del brazo óptimo."""

    selected = _as_actions(actions)
    if not isinstance(optimal_arm, (int, np.integer)) or isinstance(
        optimal_arm,
        bool,
    ):
        raise TypeError("optimal_arm debe ser un índice entero.")
    if optimal_arm < 0:
        raise ValueError("optimal_arm no puede ser negativo.")
    hits = selected == optimal_arm
    counts = np.arange(1, selected.size + 1, dtype=np.float64)
    return 100.0 * np.cumsum(hits) / counts
