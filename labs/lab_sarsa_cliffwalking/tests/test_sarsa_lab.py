import gymnasium as gym
import numpy as np
import pytest

from labs.lab_sarsa_cliffwalking.sarsa_lab import (
    epsilon_greedy_policy,
    greedy_policy,
    moving_average,
    policy_grid,
    random_policy,
    rollout_policy,
    softmax_policy,
    train_sarsa,
)


def test_policies_return_valid_actions() -> None:
    q_values = np.array([0.0, 2.0, 1.0, -1.0])
    rng = np.random.default_rng(2026)

    assert greedy_policy(q_values, rng) == 1
    assert 0 <= random_policy(q_values, rng) < 4
    assert 0 <= epsilon_greedy_policy(q_values, rng, epsilon=0.2) < 4
    assert 0 <= softmax_policy(q_values, rng, temperature=0.5) < 4


@pytest.mark.parametrize("epsilon", [-0.1, 1.1])
def test_epsilon_greedy_rejects_invalid_epsilon(epsilon: float) -> None:
    with pytest.raises(ValueError, match="epsilon"):
        epsilon_greedy_policy(
            np.zeros(4), np.random.default_rng(0), epsilon=epsilon
        )


def test_sarsa_is_reproducible_and_learns_a_successful_route() -> None:
    env_a = gym.make("CliffWalking-v1")
    env_b = gym.make("CliffWalking-v1")
    result_a = train_sarsa(
        env_a,
        episodes=600,
        alpha=0.5,
        gamma=1.0,
        epsilon=0.1,
        seed=2026,
    )
    result_b = train_sarsa(
        env_b,
        episodes=600,
        alpha=0.5,
        gamma=1.0,
        epsilon=0.1,
        seed=2026,
    )

    assert result_a.q_table.shape == (48, 4)
    assert np.array_equal(result_a.q_table, result_b.q_table)
    assert np.array_equal(result_a.rewards, result_b.rewards)

    evaluation_env = gym.make("CliffWalking-v1")
    states, reward = rollout_policy(evaluation_env, result_a.q_table)
    assert states[-1] == 47
    assert reward > -200


def test_helpers_produce_expected_shapes() -> None:
    averages = moving_average(np.arange(5, dtype=float), window=3)
    assert averages.shape == (5,)
    assert np.isnan(averages[:2]).all()
    assert np.allclose(averages[2:], [1.0, 2.0, 3.0])

    grid = policy_grid(np.zeros((48, 4)))
    assert len(grid) == 4
    assert all(len(row) == 12 for row in grid)
    assert grid[3][0] == "S"
    assert grid[3][1] == "C"
    assert grid[3][11] == "G"
