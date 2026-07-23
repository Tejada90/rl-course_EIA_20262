# Laboratorio en clase — SARSA con CliffWalking

Este laboratorio permite experimentar con **SARSA tabular** mediante la
interfaz estándar de Gymnasium. No es un reto evaluable: el algoritmo se
entrega funcionando para que la clase pueda concentrarse en cambiar políticas,
ejecutar experimentos e interpretar resultados.

## Objetivos

Al finalizar la sesión, el estudiante podrá:

- reconocer la secuencia `S, A, R, S', A'`;
- explicar por qué SARSA es un método *on-policy*;
- modificar una política de selección de acciones;
- comparar políticas aleatoria, greedy, ε-greedy y softmax;
- relacionar exploración, recompensa y caídas al precipicio;
- leer una política tabular representada mediante flechas;
- seguir visualmente la ruta greedy final y reconocer si alcanzó la meta.

## Duración sugerida

Entre 60 y 90 minutos:

| Momento | Tiempo |
|---|---:|
| Reconocer el entorno | 10 min |
| Leer y ejecutar SARSA | 15 min |
| Modificar políticas | 25 min |
| Comparar experimentos | 20 min |
| Discusión y conclusiones | 10–20 min |

## Cómo abrirlo

Desde la raíz del repositorio, dentro del Dev Container:

```bash
jupyter lab
```

Abre:

```text
labs/lab_sarsa_cliffwalking/laboratorio_sarsa.ipynb
```

También puedes ejecutar y validar todas las celdas sin abrir el navegador:

```bash
jupyter nbconvert \
  --to notebook \
  --execute labs/lab_sarsa_cliffwalking/laboratorio_sarsa.ipynb \
  --output laboratorio_sarsa_ejecutado.ipynb \
  --ExecutePreprocessor.timeout=120
```

El archivo ejecutado se crea junto al notebook y puede eliminarse después de
la revisión.

## Qué deben modificar los estudiantes

Las celdas marcadas con `🧪 ACTIVIDAD` indican exactamente dónde trabajar. Las
actividades principales son:

1. Cambiar `epsilon` y predecir qué ocurrirá.
2. Elegir otra política en la configuración.
3. Completar tres decisiones de una política ε-greedy guiada.
4. Modificar una segunda política funcional para experimentar sin bloquearse.
5. Comparar métricas utilizando la misma semilla.
6. Escribir una conclusión breve basada en evidencia.

Después de cada entrenamiento principal aparece una visualización de dos
paneles:

- valores `max Q(s,a)` y acción greedy de cada estado;
- ruta greedy final con orden de visita, pasos, recompensa y estado de llegada.

La comparación final repite esta visualización para las cuatro políticas.

No es necesario modificar `sarsa_lab.py` durante la clase. Ese archivo contiene
la implementación de referencia y permite que todos partan de un experimento
funcional.

## Guía para el docente

Antes de la clase:

1. Ejecuta el notebook completo.
2. Reinicia el kernel y borra las salidas si quieres una demostración limpia.
3. Explica que `C` representa el precipicio, `S` el inicio y `G` la meta.
4. Relaciona el mapa numerado con `S = 36`, `G = 47` y los estados `37–46`.
5. Conserva la misma semilla al comparar políticas.
6. En la actividad ε-greedy, deja que intenten los tres espacios antes de abrir
   la solución desplegable.
7. Aclara que las rutas mostradas son evaluaciones greedy posteriores al
   entrenamiento; no representan todos los recorridos exploratorios observados
   mientras el agente aprendía.

Preguntas para orientar la discusión:

- ¿Por qué una política greedy puede aprender lentamente desde una tabla Q en
  ceros?
- ¿Qué ocurre si `epsilon = 1`?
- ¿Qué diferencia hay entre explorar durante entrenamiento y usar la política
  final?
- ¿Una recompensa alta en un solo episodio demuestra que una política es
  mejor?
- ¿Por qué SARSA puede preferir una ruta alejada del precipicio?

## Archivos

- `laboratorio_sarsa.ipynb`: experiencia guiada para estudiantes.
- `sarsa_lab.py`: políticas, entrenamiento, métricas y visualización tabular.
- `tests/test_sarsa_lab.py`: validaciones técnicas del material.
