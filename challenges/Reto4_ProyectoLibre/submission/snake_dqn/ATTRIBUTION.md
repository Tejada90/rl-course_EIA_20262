# Atribución del código base

Todo el contenido de esta carpeta (`snake_dqn/`) **no es de mi autoría**. Fue tomado
íntegramente del repositorio público de Rafael Stekolshchik:

- **Repositorio:** https://github.com/Rafael1s/Deep-Reinforcement-Learning-Algorithms
- **Subproyecto:** `Snake-Pygame-DQN`
- **Commit exacto:** `85b1148de13cd5a2a46cce016412f783163e50a0`
- **URL directa:** https://github.com/Rafael1s/Deep-Reinforcement-Learning-Algorithms/tree/85b1148de13cd5a2a46cce016412f783163e50a0/Snake-Pygame-DQN
- **Fecha de descarga:** 2026-08-20

A su vez, el autor original declara en su `README.md` que partes del código se basan en
https://github.com/stefanlclarke/Snake-AI-DQN

## Nota sobre licencia

El repositorio de origen **no incluye un archivo LICENSE**. Se reproduce aquí únicamente
con fines académicos, sin ánimo de lucro, dentro del Reto 4 (proyecto libre) del curso de
Aprendizaje por Refuerzo de la Universidad EIA, y con atribución explícita al autor original.

## Archivos tomados sin modificación

```
Game.py                       Ambiente del juego (serpiente, manzana, colisiones)
model.py                      Red Q (MLP 4 capas) + construcción del vector de estado
replay_buffer.py              Memoria de repetición
Snake-DQN_lr0.0001.ipynb      Notebook de entrenamiento original (lr = 1e-4, 50.000 episodios)
Snake-DQN_lr0.00001.ipynb     Notebook de entrenamiento original (lr = 1e-5, 60.000 episodios)
WatchAgent.ipynb              Visualización del agente entrenado con Pygame
WatchAgent-with-Video.ipynb   Igual que el anterior, grabando video
README.md                     README original del autor
dir_chk_lr0.0001/             Checkpoints entrenados por el autor (30.000 a 50.000 episodios)
dir_chk_lr0.00001/            Checkpoints entrenados por el autor (40.000 a 60.000 episodios)
images/                       Gráficas de resultados publicadas por el autor
```

**Estos archivos se conservan intactos a propósito**, para que el notebook del reto pueda
compararlos contra la versión corregida y documentar las diferencias. Mi aporte —análisis,
diagnóstico, correcciones y conclusiones— vive en `../reto_04_garces_simon.ipynb`, y las
modificaciones se implementan allí sin tocar estos archivos.
