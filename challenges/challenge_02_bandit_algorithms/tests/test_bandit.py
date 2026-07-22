"""Pruebas públicas del entorno gaussiano."""

import numpy as np
import pytest

from challenges.challenge_02_bandit_algorithms.starter_code import GaussianBandit


def test_bandit_exposes_expected_properties() -> None:
    bandit = GaussianBandit([1.0, 2.0, 1.5], [0.5, 0.5, 1.5], seed=42)

    assert bandit.n_arms == 3
    assert bandit.optimal_arm == 1
    assert bandit.optimal_mean == 2.0


def test_bandit_is_reproducible() -> None:
    first = GaussianBandit([1.0, 2.0], 0.5, seed=2026)
    second = GaussianBandit([1.0, 2.0], 0.5, seed=2026)

    first_rewards = [first.pull(0) for _ in range(20)]
    second_rewards = [second.pull(0) for _ in range(20)]

    assert first_rewards == second_rewards


def test_bandit_samples_approximate_parameters() -> None:
    bandit = GaussianBandit([1.5], [0.75], seed=7)
    rewards = np.array([bandit.pull(0) for _ in range(50_000)])

    assert rewards.mean() == pytest.approx(1.5, abs=0.02)
    assert rewards.std(ddof=1) == pytest.approx(0.75, abs=0.02)


@pytest.mark.parametrize("arm", [-1, 2])
def test_bandit_rejects_unknown_arm(arm: int) -> None:
    bandit = GaussianBandit([1.0, 2.0], 0.5)

    with pytest.raises(ValueError, match="arm debe estar entre"):
        bandit.pull(arm)


@pytest.mark.parametrize("arm", [True, 0.5, "0"])
def test_bandit_rejects_non_integer_arm(arm: object) -> None:
    bandit = GaussianBandit([1.0, 2.0], 0.5)

    with pytest.raises(TypeError, match="índice entero"):
        bandit.pull(arm)  # type: ignore[arg-type]


@pytest.mark.parametrize(
    ("means", "stds"),
    [([], 1.0), ([1.0, np.nan], 1.0), ([1.0, 2.0], [0.5]), ([1.0], 0.0)],
)
def test_bandit_validates_parameters(
    means: list[float],
    stds: float | list[float],
) -> None:
    with pytest.raises(ValueError):
        GaussianBandit(means, stds)
