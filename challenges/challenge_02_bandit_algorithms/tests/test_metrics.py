"""Pruebas públicas de las métricas de comparación."""

import numpy as np
import pytest

from challenges.challenge_02_bandit_algorithms.starter_code import (
    cumulative_average,
    cumulative_regret,
    optimal_action_rate,
)


def test_cumulative_average() -> None:
    result = cumulative_average([1.0, 3.0, 2.0])

    np.testing.assert_allclose(result, [1.0, 2.0, 2.0])


def test_cumulative_regret() -> None:
    result = cumulative_regret([0, 1, 2, 1], [1.0, 2.0, 1.5])

    np.testing.assert_allclose(result, [1.0, 1.0, 1.5, 1.5])


def test_optimal_action_rate() -> None:
    result = optimal_action_rate([0, 1, 1, 2], optimal_arm=1)

    np.testing.assert_allclose(result, [0.0, 50.0, 200.0 / 3.0, 50.0])


@pytest.mark.parametrize(
    ("function", "args"),
    [
        (cumulative_average, ([],)),
        (cumulative_regret, ([0, 3], [1.0, 2.0])),
        (optimal_action_rate, ([0, 1], -1)),
    ],
)
def test_metrics_reject_invalid_inputs(
    function: object,
    args: tuple[object, ...],
) -> None:
    with pytest.raises(ValueError):
        function(*args)  # type: ignore[operator]
