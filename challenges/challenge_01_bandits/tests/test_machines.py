"""Pruebas públicas de la configuración del reto 01."""

import numpy as np
import pytest

from challenges.challenge_01_bandits.starter_code.machines import (
    MACHINES,
    reward,
)


def test_three_machines_are_defined() -> None:
    """Deben existir exactamente las tres máquinas del enunciado."""

    assert set(MACHINES) == {"A1", "A2", "A3"}


@pytest.mark.parametrize(
    ("arm", "expected_mean", "expected_std"),
    [
        ("A1", 1.0, 0.5),
        ("A2", 2.0, 0.5),
        ("A3", 1.5, 1.5),
    ],
)
def test_machine_parameters(
    arm: str,
    expected_mean: float,
    expected_std: float,
) -> None:
    """Los parámetros deben coincidir con el enunciado."""

    assert MACHINES[arm]["mean"] == expected_mean
    assert MACHINES[arm]["std"] == expected_std


@pytest.mark.parametrize("arm", ["A1", "A2", "A3"])
def test_reward_returns_float(arm: str) -> None:
    """La recompensa debe ser un número decimal."""

    rng = np.random.default_rng(42)

    result = reward(arm, rng=rng)

    assert isinstance(result, float)


def test_reward_is_reproducible() -> None:
    """La misma semilla debe generar la misma secuencia."""

    first_rng = np.random.default_rng(123)
    second_rng = np.random.default_rng(123)

    first_results = [reward("A1", rng=first_rng) for _ in range(10)]
    second_results = [reward("A1", rng=second_rng) for _ in range(10)]

    assert first_results == second_results


def test_unknown_machine_raises_error() -> None:
    """Debe producirse un error claro para una máquina inexistente."""

    with pytest.raises(ValueError, match="Máquina desconocida"):
        reward("A4")


def test_non_string_machine_raises_error() -> None:
    """El identificador de la máquina debe ser texto."""

    with pytest.raises(TypeError):
        reward(1)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("arm", "expected_mean", "expected_std"),
    [
        ("A1", 1.0, 0.5),
        ("A2", 2.0, 0.5),
        ("A3", 1.5, 1.5),
    ],
)
def test_simulated_statistics_approximate_parameters(
    arm: str,
    expected_mean: float,
    expected_std: float,
) -> None:
    """Una muestra grande debe aproximarse a los parámetros reales."""

    rng = np.random.default_rng(2026)

    samples = np.array(
        [reward(arm, rng=rng) for _ in range(50_000)]
    )

    assert np.mean(samples) == pytest.approx(expected_mean, abs=0.03)
    assert np.std(samples, ddof=1) == pytest.approx(
        expected_std,
        abs=0.03,
    )
