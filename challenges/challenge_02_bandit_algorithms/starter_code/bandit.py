"""Entorno gaussiano reutilizable para experimentos de bandits."""

from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from numpy.typing import ArrayLike, NDArray


class GaussianBandit:
    """Bandit estacionario cuyas recompensas siguen distribuciones normales.

    Parameters
    ----------
    means:
        Media real de la recompensa de cada brazo.
    stds:
        Desviación estándar positiva de cada brazo. Puede ser un escalar o una
        secuencia con la misma longitud de ``means``.
    seed:
        Semilla utilizada por el generador aleatorio de NumPy.
    """

    def __init__(
        self,
        means: ArrayLike,
        stds: float | Sequence[float],
        seed: int | None = None,
    ) -> None:
        self.means = self._validate_means(means)
        self.stds = self._validate_stds(stds, self.means.size)
        self.rng = np.random.default_rng(seed)

    @staticmethod
    def _validate_means(means: ArrayLike) -> NDArray[np.float64]:
        values = np.asarray(means, dtype=np.float64)
        if values.ndim != 1 or values.size == 0:
            raise ValueError("means debe ser un arreglo unidimensional no vacío.")
        if not np.all(np.isfinite(values)):
            raise ValueError("means solo puede contener valores finitos.")
        return values.copy()

    @staticmethod
    def _validate_stds(
        stds: float | Sequence[float],
        n_arms: int,
    ) -> NDArray[np.float64]:
        values = np.asarray(stds, dtype=np.float64)
        if values.ndim == 0:
            values = np.full(n_arms, values.item(), dtype=np.float64)
        if values.ndim != 1 or values.size != n_arms:
            raise ValueError("stds debe ser escalar o tener una entrada por brazo.")
        if not np.all(np.isfinite(values)) or np.any(values <= 0):
            raise ValueError("Todas las desviaciones deben ser finitas y positivas.")
        return values.copy()

    @property
    def n_arms(self) -> int:
        """Número de brazos disponibles."""

        return int(self.means.size)

    @property
    def optimal_arm(self) -> int:
        """Índice del primer brazo con mayor recompensa esperada."""

        return int(np.argmax(self.means))

    @property
    def optimal_mean(self) -> float:
        """Mayor recompensa esperada entre todos los brazos."""

        return float(self.means[self.optimal_arm])

    def pull(self, arm: int) -> float:
        """Genera una recompensa para el brazo indicado."""

        if not isinstance(arm, (int, np.integer)) or isinstance(arm, bool):
            raise TypeError("arm debe ser un índice entero.")
        if arm < 0 or arm >= self.n_arms:
            raise ValueError(f"arm debe estar entre 0 y {self.n_arms - 1}.")
        return float(self.rng.normal(self.means[arm], self.stds[arm]))
