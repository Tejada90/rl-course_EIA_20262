# Reto 03 — Q-Learning y estrategias de exploración

## 1. Propósito

En este reto se estudiará cómo la estrategia de exploración modifica el
aprendizaje de un agente Q-Learning. A diferencia del reto de bandits, la
acción adecuada depende ahora del estado y puede afectar recompensas futuras.

Se compararán cuatro alternativas:

1. ε-greedy.
2. ε-greedy con inicialización optimista.
3. UCB (*Upper Confidence Bound*) por estado–acción.
4. Softmax o selección de Boltzmann.

La pregunta guía es:

> ¿Cómo cambia la velocidad de aprendizaje y la calidad de la política final
> al usar diferentes mecanismos de exploración en problemas con dinámicas y
> recompensas distintas?

El reto está diseñado para dos clases de trabajo. La primera se dedica a la
implementación y verificación; la segunda, al experimento, análisis y
comunicación de resultados.

## 2. Objetivos de aprendizaje

Al finalizar, el estudiante estará en capacidad de:

- Implementar Q-Learning tabular usando correctamente la API de Gymnasium.
- Diferenciar selección de acciones, actualización de valor y evaluación.
- Adaptar ε-greedy, optimismo, UCB y Softmax a pares estado–acción.
- Tratar correctamente estados terminales y episodios truncados.
- Diseñar comparaciones reproducibles mediante semillas y presupuestos iguales.
- Distinguir desempeño durante entrenamiento y calidad de la política final.
- Reportar incertidumbre experimental y no depender de una sola corrida.
- Interpretar cómo la estructura del entorno afecta la exploración.

## 3. Escenarios de Gymnasium

### 3.1 FrozenLake-v1

El agente debe llegar desde el inicio hasta una meta evitando huecos. Se usa
`is_slippery=True`, por lo que la acción ejecutada puede producir un movimiento
distinto al esperado.

- Observación: posición discreta en una cuadrícula 4 × 4.
- Acciones: izquierda, abajo, derecha y arriba.
- Recompensa: 1 al llegar a la meta y 0 en los demás pasos.
- Dificultad: recompensa escasa, transiciones estocásticas y muchos episodios
  sin señal positiva.

### 3.2 Blackjack-v1

El agente decide si pide otra carta o se planta. Se usa `sab=True`, que sigue
la formulación empleada en Sutton y Barto.

- Observación: `(suma_jugador, carta_visible_crupier, as_utilizable)`.
- Acciones: plantarse (`0`) o pedir carta (`1`).
- Recompensas: -1 al perder, 0 al empatar y 1 al ganar.
- Dificultad: el estado es una tupla, la recompensa llega al final y la misma
  suma puede requerir decisiones distintas según la carta del crupier y el as.

La observación compuesta se convierte en un índice único mediante
`numpy.ravel_multi_index`. El notebook suministra esta función para que el foco
del reto continúe siendo Q-Learning. El espacio declarado por Gymnasium tiene
`32 × 11 × 2 = 704` combinaciones; algunas no son alcanzables, lo cual también
es relevante para interpretar UCB y la inicialización optimista.

### 3.3 Taxi-v4

El agente debe recoger un pasajero y dejarlo en el destino correcto.

- Observación: 500 estados discretos que codifican taxi, pasajero y destino.
- Acciones: cuatro movimientos, recoger y dejar pasajero.
- Recompensas: -1 por paso, +20 por entrega correcta y -10 por recoger o dejar
  ilegalmente.
- Dificultad: espacio mayor, recompensas negativas y acciones contextuales.

Estos tres escenarios permiten contrastar recompensa escasa, resultado terminal
estocástico y control secuencial con penalizaciones. `CliffWalking-v1` no se usa
porque ya fue trabajado previamente en el curso.

## 4. Fundamento de Q-Learning

Para cada transición se actualiza únicamente el par visitado:

```text
Q(S_t,A_t) ← Q(S_t,A_t)
             + α [R_(t+1) + γ (1-d) max_a Q(S_(t+1),a) - Q(S_t,A_t)]
```

`α` controla la magnitud de cada actualización, `γ` descuenta recompensas
futuras y `d` vale uno cuando la transición terminó el MDP. No debe realizarse
*bootstrap* desde un estado terminal.

Gymnasium distingue:

- `terminated`: se alcanzó un estado terminal definido por el problema.
- `truncated`: el episodio fue detenido por un límite externo, como máximo de
  pasos.

El estudiante debe documentar si realiza *bootstrap* ante truncamiento y usar
la decisión de manera consistente. El ciclo del episodio siempre se detiene
cuando `terminated or truncated`.

## 5. Estrategias obligatorias

### 5.1 ε-greedy

Con probabilidad ε se selecciona una acción uniforme al azar. En otro caso se
elige una acción de máximo valor. Los empates deben resolverse aleatoriamente.

Comparación base: `ε = 0.10`, `Q0 = 0`.

### 5.2 ε-greedy con inicialización optimista

Se emplea la misma regla, pero la tabla se inicializa con valores mayores a los
esperados. Las acciones no probadas parecen atractivas y pierden optimismo al
ser actualizadas con experiencia real.

Comparación base: `ε = 0.01`, `Q0 = 5`.

El ε pequeño evita depender exclusivamente del optimismo en estados que el
agente visita tarde. El estudiante debe discutir por qué `Q0 = 5` puede tener
efectos diferentes en FrozenLake, Blackjack y Taxi.

### 5.3 UCB por estado–acción

Para el estado actual se usa:

```text
Q(s,a) + c sqrt(log(N(s) + 1) / N(s,a))
```

Antes de aplicar la fórmula se eligen acciones no visitadas. `N(s,a)` cuenta
selecciones de la acción en ese estado y `N(s)` es la suma sobre acciones.

Comparación base: `c = 1`.

Los conteos son locales al estado; no se debe usar un único conteo global. En
Blackjack habrá estados declarados pero inalcanzables, que nunca deben afectar
la selección en un estado observado.

### 5.4 Softmax

Las acciones se muestrean con probabilidad proporcional a:

```text
exp(Q(s,a) / τ)
```

Debe usarse la versión numéricamente estable:

```python
logits = q[state] / temperature
weights = np.exp(logits - np.max(logits))
probabilities = weights / weights.sum()
```

La temperatura debe ser positiva. Valores bajos concentran la probabilidad en
acciones de alto valor; valores altos aproximan una distribución uniforme.

Comparación base: `τ = 0.50`.

## 6. Organización de las dos clases

### Clase 1 — Implementación y verificación

1. Ejecutar y describir los tres entornos.
2. Comprender la codificación de observaciones de Blackjack.
3. Implementar `random_argmax` y `select_action`.
4. Implementar `train_q_learning`.
5. Escribir pruebas pequeñas y corregir errores.
6. Ejecutar el piloto de FrozenLake.

Al terminar la clase deben existir cuatro selectores válidos, un ciclo de
entrenamiento funcional y una corrida piloto reproducible.

### Clase 2 — Experimento y análisis

1. Implementar la evaluación greedy sin aprendizaje.
2. Ejecutar la comparación principal.
3. Construir tabla y visualizaciones.
4. Realizar análisis de sensibilidad.
5. Responder las preguntas y escribir conclusiones.
6. Reiniciar, ejecutar y exportar el notebook.

## 7. Contratos de implementación

### `random_argmax(values, rng)`

- Devuelve un entero correspondiente a un máximo.
- Si hay varios máximos, no favorece siempre el primero.
- No modifica el arreglo recibido.

### `select_action(q, counts, state, strategy, rng, ...)`

- Acepta exactamente las cuatro estrategias solicitadas.
- Devuelve una acción dentro del rango de columnas de `q`.
- Valida `0 <= epsilon <= 1`, `c >= 0` y `temperature > 0`.
- Usa únicamente la fila correspondiente al estado actual.
- No modifica `q` ni `counts`.

### `train_q_learning(...)`

- Crea un entorno independiente para la corrida.
- Inicializa Q con el `q0` indicado y los conteos con cero.
- Codifica toda observación antes de indexar la tabla.
- Incrementa `counts[state, action]` exactamente una vez por transición.
- Actualiza solo el par estado–acción seleccionado.
- No realiza *bootstrap* desde estados terminales.
- Respeta `max_steps`, cierra el entorno y controla las semillas.
- Devuelve Q, historial por episodio y conteos.
- El historial contiene `episode`, `return`, `length`, `success` y
  `td_error_mean`.

### `evaluate_policy(...)`

- Selecciona acciones greedy con desempate aleatorio.
- No explora ni modifica Q.
- Usa semillas distintas a las de entrenamiento.
- Devuelve una fila por episodio con retorno, longitud y éxito.

## 8. Semillas y comparación justa

La semilla base es `2026`. Para la corrida `r` se recomienda:

```text
semilla_entrenamiento = 2026 + r
semilla_evaluación = 1_000_000 + 2026 + r
```

Cada estrategia debe recibir la misma lista de semillas por entorno. Esto no
significa compartir un objeto generador entre algoritmos: cada corrida crea su
propio generador con la semilla correspondiente.

Configuración mínima:

| Entorno | Episodios por corrida | Máximo de pasos |
|---|---:|---:|
| FrozenLake-v1 | 2.000 | 100 |
| Blackjack-v1 | 10.000 | 100 |
| Taxi-v4 | 2.000 | 200 |

- Corridas independientes: mínimo 30.
- Episodios de evaluación por política: 100.
- Valores base: `α = 0.10`, `γ = 0.99`.

Blackjack usa más episodios porque cada episodio es corto y la recompensa
terminal presenta alta variabilidad.

## 9. Verificaciones mínimas

Antes del experimento completo compruebe mediante `assert`:

- La tabla tiene forma `(n_states, n_actions)`.
- Todos los valores de Q son finitos.
- El historial tiene exactamente una fila por episodio.
- Las longitudes están entre 1 y `max_steps`.
- La suma de conteos coincide con el número de transiciones.
- Las acciones seleccionadas son válidas.
- Una misma semilla reproduce Q e historial.
- Cambiar la semilla puede producir resultados distintos.
- Una transición terminal usa la recompensa como objetivo.
- Con `γ = 0`, el objetivo ignora el siguiente estado.
- La evaluación no altera la tabla Q.

## 10. Métricas obligatorias

Por entorno y algoritmo reporte:

1. Retorno medio del último 10 % del entrenamiento.
2. Área bajo la curva del retorno medio.
3. Tasa de éxito de evaluación.
4. Retorno medio de evaluación.
5. Longitud media de evaluación.
6. Intervalo de confianza del 95 % entre corridas.

Defina explícitamente `success` en cada entorno. Una opción válida es:

- FrozenLake: retorno del episodio igual a 1.
- Blackjack: retorno del episodio igual a 1.
- Taxi: entrega correcta, identificable por recompensa terminal positiva.

No construya una única media de retornos mezclando entornos, pues sus escalas
y significados son diferentes.

## 11. Visualizaciones obligatorias

Incluya al menos:

1. Retorno por episodio, suavizado y con banda de IC 95 %.
2. Tasa de éxito móvil o acumulada.
3. Retorno de evaluación por entorno y algoritmo.
4. Visualización de una política o mapa de `max_a Q(s,a)`.

Todas las figuras deben incluir título, nombres de ejes, unidades y leyenda. El
suavizado no reemplaza los datos originales ni la medida de incertidumbre.

## 12. Sensibilidad de hiperparámetros

Elija el entorno en el que las estrategias difieran más. Use al menos 10
corridas por configuración y conserve constantes episodios, α, γ y semillas.

| Estrategia | Valores |
|---|---|
| ε-greedy | ε ∈ {0.01, 0.10, 0.30} |
| Optimista | Q0 ∈ {1, 5, 10}, ε = 0.01 |
| UCB | c ∈ {0.25, 1, 2} |
| Softmax | τ ∈ {0.10, 0.50, 1.0} |

La selección de la mejor configuración debe basarse en resultados agregados,
no en una corrida favorable.

## 13. Preguntas de interpretación

Las respuestas deben citar valores, tablas o figuras:

1. ¿Qué estrategia aprendió más rápido en cada entorno?
2. ¿La mejor curva de entrenamiento produjo la mejor política greedy?
3. ¿Dónde ayudó o perjudicó la inicialización optimista?
4. ¿Cómo se comportó UCB en estados poco visitados?
5. ¿Cómo afectó la temperatura a Softmax?
6. ¿Qué estrategia fue más sensible a FrozenLake estocástico?
7. ¿Qué diferencias surgieron en Blackjack entre manos con y sin as utilizable?
8. ¿Existe un ganador para todos los escenarios y métricas?
9. ¿Qué recomendaría si interactuar con el entorno fuera costoso?
10. ¿Cuáles son dos amenazas a la validez del experimento?

## 14. Uso responsable de inteligencia artificial

El notebook debe documentar herramienta, prompts, sugerencias aceptadas o
rechazadas, cambios manuales y método de verificación. El estudiante continúa
siendo responsable de comprender, ejecutar y explicar el código entregado.

## 15. Entrega

Trabaje en:

```text
challenges/challenge_03_qlearning_exploration/submission/reto_03_apellido_nombre.ipynb
```

Exporte a:

```text
challenges/challenge_03_qlearning_exploration/submission/exports/reto_03_apellido_nombre.html
```

No use espacios, tildes, eñes ni mayúsculas en los nombres. Antes de entregar:

1. Reinicie el kernel y ejecute todas las celdas.
2. Confirme que no haya excepciones ni resultados manualmente alterados.
3. Revise tablas, figuras e interpretaciones.
4. Exporte y abra el HTML.
5. Ejecute `pytest -q` para verificar que no afectó otros retos.

## 16. Criterios de evaluación

| Criterio | Peso |
|---|---:|
| Q-Learning y tratamiento de terminales | 20 % |
| Cuatro estrategias de exploración | 20 % |
| Pruebas, semillas y diseño experimental | 15 % |
| Métricas, incertidumbre y visualizaciones | 20 % |
| Sensibilidad e interpretación | 20 % |
| Documentación, conclusiones y uso de IA | 5 % |

## 17. Lista de comprobación

- [ ] Implementé las cuatro estrategias y resolví empates aleatoriamente.
- [ ] Codifiqué correctamente las observaciones de Blackjack.
- [ ] Traté estados terminales y truncamientos de forma explícita.
- [ ] Separé entrenamiento de evaluación greedy.
- [ ] Usé presupuestos y semillas comparables.
- [ ] Ejecuté al menos 30 corridas principales.
- [ ] Reporté incertidumbre entre corridas.
- [ ] Incluí tabla, cuatro visualizaciones y sensibilidad.
- [ ] Respondí todas las preguntas con evidencia.
- [ ] Documenté el uso de IA y redacté entre cuatro y seis conclusiones.
- [ ] Ejecuté el notebook desde cero y revisé el HTML.

## 18. Viabilidad técnica verificada

El diseño fue comprobado con la versión fijada en `requirements.txt`:
Gymnasium 1.3.0 y Python 3.11 dentro del contenedor del curso.

La validación de referencia ejecutó las cuatro estrategias en los tres
entornos, comprobó formas de Q, valores finitos y correspondencia entre conteos
y transiciones. También se ejecutó una corrida completa con los presupuestos
de episodios de la tabla. En el equipo de validación tardó aproximadamente 23
segundos; 30 corridas secuenciales equivalen a cerca de 12 minutos, aunque el
tiempo exacto depende del hardware.

Durante esta comprobación se confirmó que Gymnasium 1.3.0 requiere `Taxi-v4`.
La versión anterior `Taxi-v3` produce `DeprecatedEnv` y por esa razón no aparece
en el reto.

El reto es realizable con las dependencias y el contenedor suministrados. Esta
garantía cubre compatibilidad de API, dimensiones, ejecución de los algoritmos
y presupuesto computacional; la calidad de los resultados entregados continúa
dependiendo de que el estudiante complete correctamente los `TODO`.
