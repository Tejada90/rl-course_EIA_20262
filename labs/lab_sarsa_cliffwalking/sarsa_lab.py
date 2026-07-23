"""Herramientas sencillas para experimentar con SARSA en CliffWalking.

Las funciones priorizan claridad sobre abstracciones avanzadas. El notebook del
laboratorio permite cambiar la política de selección sin modificar el ciclo de
entrenamiento.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import gymnasium as gym
import numpy as np
from numpy.typing import NDArray

QTable = NDArray[np.float64]
RandomGenerator = np.random.Generator
Policy = Callable[..., int]


@dataclass(frozen=True)
class TrainingResult:
    """Resultados necesarios para analizar una corrida de SARSA."""

    q_table: QTable
    rewards: NDArray[np.float64]
    episode_lengths: NDArray[np.int64]
    cliff_falls: NDArray[np.int64]


def _validate_q_values(q_values: NDArray[np.float64]) -> None:
    if q_values.ndim != 1 or q_values.size == 0:
        raise ValueError("q_values debe ser un arreglo unidimensional no vacío.")
    if not np.all(np.isfinite(q_values)):
        raise ValueError("q_values solo puede contener valores finitos.")


def _random_argmax(
    q_values: NDArray[np.float64], rng: RandomGenerator
) -> int:
    """Elige aleatoriamente entre acciones empatadas con el valor máximo."""

    best_actions = np.flatnonzero(q_values == np.max(q_values))
    return int(rng.choice(best_actions))


def random_policy(
    q_values: NDArray[np.float64],
    rng: RandomGenerator,
    **_: float,
) -> int:
    """Selecciona todas las acciones con la misma probabilidad."""

    _validate_q_values(q_values)
    return int(rng.integers(q_values.size))


def greedy_policy(
    q_values: NDArray[np.float64],
    rng: RandomGenerator,
    **_: float,
) -> int:
    """Selecciona una acción de máximo valor y resuelve empates al azar."""

    _validate_q_values(q_values)
    return _random_argmax(q_values, rng)


def epsilon_greedy_policy(
    q_values: NDArray[np.float64],
    rng: RandomGenerator,
    epsilon: float = 0.1,
    **_: float,
) -> int:
    """Explora con probabilidad epsilon y explota en caso contrario."""

    _validate_q_values(q_values)
    if not 0.0 <= epsilon <= 1.0:
        raise ValueError("epsilon debe estar entre 0 y 1.")
    if rng.random() < epsilon:
        return int(rng.integers(q_values.size))
    return _random_argmax(q_values, rng)


def softmax_policy(
    q_values: NDArray[np.float64],
    rng: RandomGenerator,
    temperature: float = 1.0,
    **_: float,
) -> int:
    """Muestrea acciones según una distribución softmax estable."""

    _validate_q_values(q_values)
    if not np.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature debe ser finita y mayor que cero.")
    logits = q_values / temperature
    weights = np.exp(logits - np.max(logits))
    probabilities = weights / weights.sum()
    return int(rng.choice(q_values.size, p=probabilities))


def train_sarsa(
    env: gym.Env,
    policy: Policy = epsilon_greedy_policy,
    *,
    episodes: int = 500,
    alpha: float = 0.1,
    gamma: float = 0.99,
    seed: int = 2026,
    max_steps: int = 1_000,
    **policy_kwargs: float,
) -> TrainingResult:
    """Entrena SARSA tabular en un entorno discreto de Gymnasium.

    La política recibe los valores Q del estado actual, un generador aleatorio
    y los argumentos nombrados incluidos en ``policy_kwargs``.
    """

    if episodes <= 0:
        raise ValueError("episodes debe ser positivo.")
    if max_steps <= 0:
        raise ValueError("max_steps debe ser positivo.")
    if not 0.0 < alpha <= 1.0:
        raise ValueError("alpha debe estar en el intervalo (0, 1].")
    if not 0.0 <= gamma <= 1.0:
        raise ValueError("gamma debe estar entre 0 y 1.")
    if not isinstance(env.observation_space, gym.spaces.Discrete):
        raise TypeError("SARSA tabular requiere observaciones discretas.")
    if not isinstance(env.action_space, gym.spaces.Discrete):
        raise TypeError("SARSA tabular requiere acciones discretas.")

    n_states = int(env.observation_space.n)
    n_actions = int(env.action_space.n)
    q_table = np.zeros((n_states, n_actions), dtype=np.float64)
    rewards = np.zeros(episodes, dtype=np.float64)
    episode_lengths = np.zeros(episodes, dtype=np.int64)
    cliff_falls = np.zeros(episodes, dtype=np.int64)
    rng = np.random.default_rng(seed)

    for episode in range(episodes):
        state, _ = env.reset(seed=seed + episode)
        action = policy(q_table[state], rng, **policy_kwargs)

        for step in range(1, max_steps + 1):
            next_state, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated

            rewards[episode] += float(reward)
            episode_lengths[episode] = step
            if reward == -100:
                cliff_falls[episode] += 1

            if done:
                td_target = float(reward)
                q_table[state, action] += alpha * (
                    td_target - q_table[state, action]
                )
                break

            next_action = policy(q_table[next_state], rng, **policy_kwargs)
            td_target = float(reward) + gamma * q_table[
                next_state, next_action
            ]
            td_error = td_target - q_table[state, action]
            q_table[state, action] += alpha * td_error
            state, action = next_state, next_action

    return TrainingResult(
        q_table=q_table,
        rewards=rewards,
        episode_lengths=episode_lengths,
        cliff_falls=cliff_falls,
    )


def moving_average(
    values: NDArray[np.float64], window: int = 20
) -> NDArray[np.float64]:
    """Calcula un promedio móvil conservando la longitud de la serie."""

    data = np.asarray(values, dtype=np.float64)
    if data.ndim != 1:
        raise ValueError("values debe ser un arreglo unidimensional.")
    if window <= 0:
        raise ValueError("window debe ser positivo.")
    if data.size == 0:
        return data.copy()
    window = min(window, data.size)
    cumulative = np.cumsum(np.insert(data, 0, 0.0))
    valid = (cumulative[window:] - cumulative[:-window]) / window
    prefix = np.full(window - 1, np.nan)
    return np.concatenate((prefix, valid))


def policy_grid(q_table: QTable) -> list[list[str]]:
    """Convierte la política greedy de CliffWalking en una cuadrícula de flechas."""

    values = np.asarray(q_table, dtype=np.float64)
    if values.shape != (48, 4):
        raise ValueError("CliffWalking requiere una tabla Q con forma (48, 4).")

    arrows = np.array(["↑", "→", "↓", "←"])
    grid = arrows[np.argmax(values, axis=1)].reshape(4, 12).tolist()
    grid[3][0] = "S"
    for column in range(1, 11):
        grid[3][column] = "C"
    grid[3][11] = "G"
    return grid


def rollout_policy(
    env: gym.Env,
    q_table: QTable,
    *,
    seed: int = 2026,
    max_steps: int = 200,
) -> tuple[list[int], float]:
    """Ejecuta una política greedy entrenada y devuelve estados y recompensa."""

    state, _ = env.reset(seed=seed)
    states = [int(state)]
    total_reward = 0.0

    for _ in range(max_steps):
        action = int(np.argmax(q_table[state]))
        state, reward, terminated, truncated, _ = env.step(action)
        states.append(int(state))
        total_reward += float(reward)
        if terminated or truncated:
            break

    return states, total_reward
