"""Configuración base de las máquinas del reto 01."""

from __future__ import annotations

import numpy as np


MACHINES: dict[str, dict[str, float]] = {
    "A1": {"mean": 1.0, "std": 0.5},
    "A2": {"mean": 2.0, "std": 0.5},
    "A3": {"mean": 1.5, "std": 1.5},
}


def reward(
    arm: str,
    rng: np.random.Generator | None = None,
) -> float:
    """Genera una recompensa para una máquina.

    Esta implementación se proporciona como referencia para las pruebas
    públicas del repositorio. En el notebook, el estudiante debe construir
    y explicar su propia implementación.

    Parameters
    ----------
    arm:
        Identificador de la máquina: ``A1``, ``A2`` o ``A3``.
    rng:
        Generador de números aleatorios de NumPy. Si no se proporciona,
        se crea uno nuevo.

    Returns
    -------
    float
        Recompensa generada por la distribución normal de la máquina.

    Raises
    ------
    TypeError
        Si ``arm`` no es una cadena de texto.
    ValueError
        Si el identificador de la máquina no existe.
    """

    if not isinstance(arm, str):
        raise TypeError("El identificador de la máquina debe ser texto.")

    if arm not in MACHINES:
        valid_arms = ", ".join(MACHINES)
        raise ValueError(
            f"Máquina desconocida: {arm}. Opciones válidas: {valid_arms}."
        )

    if rng is None:
        rng = np.random.default_rng()

    parameters = MACHINES[arm]

    return float(
        rng.normal(
            loc=parameters["mean"],
            scale=parameters["std"],
        )
    )
