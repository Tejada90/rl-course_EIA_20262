"""Ejemplo mínimo para verificar y usar el entorno Docker del curso."""

from __future__ import annotations

import gymnasium
import numpy as np
import torch

from challenges.challenge_01_bandits.starter_code.machines import MACHINES, reward


def main() -> None:
    """Muestra versiones y simula recompensas de las máquinas del reto 01."""

    print("Entorno del curso disponible")
    print(f"NumPy: {np.__version__}")
    print(f"Gymnasium: {gymnasium.__version__}")
    print(f"PyTorch: {torch.__version__}")
    print(f"CUDA disponible: {torch.cuda.is_available()}")

    rng = np.random.default_rng(seed=2026)

    print("\nMedia estimada con 1.000 recompensas por máquina:")
    for arm in MACHINES:
        samples = torch.tensor(
            [reward(arm, rng=rng) for _ in range(1_000)],
            dtype=torch.float64,
        )
        print(f"{arm}: {samples.mean().item():.3f}")


if __name__ == "__main__":
    main()
