# Reto 02 — Comparación de algoritmos para Multi-Armed Bandits

## 1. Propósito

En este reto se implementarán y compararán cuatro estrategias para resolver un
problema estacionario de máquinas tragamonedas de múltiples brazos:

1. ε-greedy.
2. ε-greedy con valores iniciales optimistas.
3. UCB (*Upper Confidence Bound*).
4. Softmax.

La pregunta guía es:

> ¿Cómo cambia el balance entre exploración y explotación según el algoritmo,
> y cuál estrategia aprende a seleccionar con mayor frecuencia la mejor
> máquina?

## 2. Objetivos de aprendizaje

Al finalizar el reto, el estudiante deberá poder:

- Implementar cuatro estrategias de selección de acciones.
- Actualizar estimaciones mediante medias incrementales.
- Explicar el balance entre exploración y explotación.
- Diseñar una comparación experimental justa y reproducible.
- Interpretar recompensa, selección óptima y regret.
- Analizar el efecto de los hiperparámetros.
- Comunicar resultados mediante tablas, curvas y conclusiones.

## 3. Entorno experimental

Se utilizarán las máquinas del Reto 1:

```text
A1 ~ Normal(media=1.0, desviación=0.5)
A2 ~ Normal(media=2.0, desviación=0.5)
A3 ~ Normal(media=1.5, desviación=1.5)
```

El brazo óptimo es `A2`, porque tiene la mayor recompensa esperada. El código
suministrado representa los brazos mediante índices:

```text
0 → A1
1 → A2
2 → A3
```

Importa el entorno y las métricas con:

```python
from challenges.challenge_02_bandit_algorithms.starter_code import (
    GaussianBandit,
    cumulative_average,
    cumulative_regret,
    optimal_action_rate,
)
```

No modifiques el código suministrado. Tu implementación debe estar en el
notebook de entrega.

## 4. Diseño mínimo del experimento

La comparación principal debe usar:

```text
Horizonte: 1.000 pasos por corrida
Corridas independientes: mínimo 100
Semilla base: 2026
Máquinas: las tres distribuciones definidas anteriormente
```

Cada algoritmo debe evaluarse con las mismas condiciones. Usa semillas
controladas y documenta cómo garantizas una comparación justa.

Parámetros base sugeridos:

| Algoritmo | Parámetros |
|---|---|
| ε-greedy | ε = 0.10, valores iniciales = 0 |
| Inicio optimista | ε = 0.00, valores iniciales = 5 |
| UCB | c = 2 |
| Softmax | temperatura τ = 0.20 |

Estos valores definen la comparación principal. En el análisis de sensibilidad
deberás probar valores adicionales.

## 5. Reglas comunes de implementación

Todos los algoritmos deben:

1. Mantener un conteo de selecciones por brazo.
2. Mantener una estimación `Q(a)` por brazo.
3. Seleccionar exactamente una acción por paso.
4. Recibir una recompensa del entorno.
5. Actualizar la acción seleccionada mediante media incremental:

```text
N(a) ← N(a) + 1
Q(a) ← Q(a) + [R - Q(a)] / N(a)
```

6. Guardar, como mínimo, paso, acción, recompensa y estimación de cada brazo.
7. Resolver empates aleatoriamente, sin favorecer siempre el primer brazo.

La salida de una corrida puede ser un `DataFrame` con esta estructura:

```text
step | action | reward | q_a1 | q_a2 | q_a3
```

## 6. Algoritmos obligatorios

### Parte 1 — ε-greedy

En cada paso:

- Con probabilidad `ε`, selecciona un brazo al azar.
- Con probabilidad `1 - ε`, selecciona un brazo con mayor estimación.

Implementa una función o clase que reciba al menos el entorno, horizonte,
`epsilon` y semilla.

### Parte 2 — ε-greedy con inicio optimista

Utiliza la misma regla de selección y actualización, pero inicializa todas las
estimaciones con un valor superior a las recompensas esperadas. En la
comparación base utiliza `Q0 = 5` y `ε = 0`.

Explica por qué los valores optimistas inducen exploración incluso sin acciones
aleatorias y por qué este efecto disminuye con el tiempo.

### Parte 3 — UCB

Después de seleccionar cada brazo al menos una vez, usa:

```text
A_t = argmax_a [Q_t(a) + c √(ln(t) / N_t(a))]
```

Debes evitar divisiones por cero. Una solución válida es seleccionar cada brazo
una vez antes de aplicar la fórmula.

Explica el papel de `c` y del término de incertidumbre.

### Parte 4 — Softmax

Convierte las estimaciones en probabilidades:

```text
P(a) = exp(Q(a) / τ) / Σ_b exp(Q(b) / τ)
```

Implementa la versión numéricamente estable, restando el máximo antes de
calcular las exponenciales:

```python
logits = q_values / temperature
weights = np.exp(logits - np.max(logits))
probabilities = weights / weights.sum()
```

La temperatura debe ser estrictamente positiva. Explica cómo cambia la
exploración cuando `τ` aumenta o disminuye.

## 7. Métricas obligatorias

Compara los algoritmos con:

- Recompensa acumulada.
- Recompensa media acumulada.
- Porcentaje acumulado de selección del brazo óptimo.
- Pseudo-regret acumulado.

El pseudo-regret instantáneo es:

```text
r* - μ(A_t)
```

donde `r*` es la mayor media real y `μ(A_t)` es la media real del brazo
seleccionado. No reemplaces esta medida por la diferencia entre recompensas
aleatorias observadas.

Promedia cada curva sobre todas las corridas independientes. Reporta también
una medida de variabilidad, como desviación estándar, error estándar o un
intervalo de confianza, e indica claramente cuál utilizaste.

## 8. Actividades del notebook

### Portada y preparación

Incluye título, nombres, correos, fecha, objetivo, librerías, constantes y
semillas.

### Verificación del entorno

Crea un `GaussianBandit`, muestra sus propiedades y genera algunas
recompensas. Explica por qué `A2` es el brazo óptimo.

### Implementación

Implementa los cuatro algoritmos. Incluye validaciones para hiperparámetros y
comentarios breves en las decisiones no evidentes.

### Pruebas pequeñas

Antes del experimento completo, verifica que cada algoritmo:

- Produzca exactamente una acción y recompensa por paso.
- Solo seleccione acciones válidas.
- Actualice los conteos hasta sumar el horizonte.
- Sea reproducible con la misma semilla.
- Pueda producir resultados diferentes con otra semilla.

### Comparación principal

Ejecuta al menos 100 corridas de 1.000 pasos para cada algoritmo. Construye una
tabla resumen con:

```text
Algoritmo
Recompensa total promedio
Recompensa promedio en los últimos 100 pasos
Porcentaje final de acción óptima
Regret acumulado final
```

### Visualizaciones

Incluye al menos cuatro gráficas comparativas:

1. Recompensa media acumulada por paso.
2. Porcentaje de selección del brazo óptimo por paso.
3. Regret acumulado por paso.
4. Conteo o proporción final de selección de cada brazo.

Todas deben incluir título, ejes, leyenda y unidades. Las curvas agregadas deben
mostrar su variabilidad mediante bandas o barras de error cuando sea posible.

### Sensibilidad de hiperparámetros

Compara al menos:

```text
ε: 0.01, 0.10 y 0.30
Q0: 2, 5 y 10
c: 0.5, 1 y 2
τ: 0.05, 0.20 y 1.0
```

Puedes usar menos corridas para esta sección si justificas la decisión, pero
mantén constantes las demás condiciones.

### Interpretación

Responde con evidencia:

1. ¿Qué algoritmo obtuvo mayor recompensa acumulada?
2. ¿Cuál identificó más rápido el brazo óptimo?
3. ¿Cuál obtuvo menor regret final?
4. ¿Qué comportamiento produjo el inicio optimista?
5. ¿Cómo cambia UCB al modificar `c`?
6. ¿Cómo cambia Softmax al modificar la temperatura?
7. ¿Cuál estrategia fue más sensible a la alta varianza de `A3`?
8. ¿Existe un algoritmo ganador para todas las métricas y horizontes?
9. ¿Qué método recomendarías y bajo qué condiciones?

### Uso de inteligencia artificial y conclusiones

Documenta las herramientas de IA, preguntas, recomendaciones, ajustes
manuales y validaciones. Incluye entre cuatro y seis conclusiones.

## 9. Eficiencia y buenas prácticas

- No imprimas información dentro de cada paso o corrida.
- Evita crear figuras dentro de los bucles de simulación.
- Almacena primero los resultados y grafica después.
- Usa arreglos de NumPy cuando simplifiquen el cálculo.
- Nombra claramente hiperparámetros, semillas y dimensiones.
- No modifiques resultados manualmente ni descartes corridas desfavorables.

## 10. Archivo de entrega

Trabaja en:

```text
challenges/challenge_02_bandit_algorithms/submission/reto_02_apellido_nombre.ipynb
```

Exporta el notebook a:

```text
challenges/challenge_02_bandit_algorithms/submission/exports/reto_02_apellido_nombre.html
```

No uses espacios, tildes, mayúsculas ni caracteres especiales en los nombres.

## 11. Archivos restringidos

No modifiques:

```text
challenges/challenge_02_bandit_algorithms/starter_code/
challenges/challenge_02_bandit_algorithms/tests/
.github/workflows/
docker/
docker-compose.yml
```

## 12. Verificación local

Ejecuta todas las celdas desde cero y luego:

```bash
pytest challenges/challenge_02_bandit_algorithms/tests -v
pytest -q
```

Exporta el notebook:

```bash
jupyter nbconvert \
  --to html \
  challenges/challenge_02_bandit_algorithms/submission/reto_02_apellido_nombre.ipynb \
  --output-dir challenges/challenge_02_bandit_algorithms/submission/exports
```

## 13. Entrega mediante GitHub

Actualiza `main` y crea una rama:

```bash
git switch main
git pull origin main
git switch -c challenge-02-nombre-apellido
```

Agrega únicamente tu notebook y HTML:

```bash
git add challenges/challenge_02_bandit_algorithms/submission/reto_02_apellido_nombre.ipynb
git add challenges/challenge_02_bandit_algorithms/submission/exports/reto_02_apellido_nombre.html
git commit -m "feat: entregar reto 02 de algoritmos bandit"
git push -u origin challenge-02-nombre-apellido
```

Crea un Pull Request hacia `main`, completa la plantilla y espera que GitHub
Actions termine correctamente.

## 14. Criterios de evaluación

| Criterio | Peso |
|---|---:|
| Implementación correcta de los cuatro algoritmos | 30 % |
| Diseño experimental y reproducibilidad | 20 % |
| Métricas, tablas y visualizaciones | 20 % |
| Interpretación y sensibilidad de hiperparámetros | 20 % |
| Documentación, conclusiones y uso responsable de IA | 10 % |

## 15. Lista de verificación

- [ ] Implementé los cuatro algoritmos.
- [ ] Resolví empates aleatoriamente.
- [ ] Usé actualizaciones incrementales.
- [ ] Ejecuté al menos 100 corridas de 1.000 pasos.
- [ ] Controlé y documenté las semillas.
- [ ] Calculé las cuatro métricas obligatorias.
- [ ] Incluí la tabla resumen y las cuatro visualizaciones.
- [ ] Analicé los hiperparámetros solicitados.
- [ ] Respondí todas las preguntas de interpretación.
- [ ] Documenté el uso de inteligencia artificial.
- [ ] Ejecuté todas las celdas desde cero.
- [ ] Todas las pruebas pasaron.
- [ ] Exporté y revisé el HTML.
- [ ] El Pull Request contiene únicamente el notebook y el HTML.
