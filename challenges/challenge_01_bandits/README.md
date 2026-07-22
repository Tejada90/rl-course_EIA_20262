# Reto 01 — Simulador de máquinas Multi-Armed Bandit

Antes de comenzar, sigue la guía completa de preparación y entrega disponible
en `docs/guia_inicio_estudiantes.md`.

## 1. Propósito

En este reto se construirá un simulador sencillo de un problema de máquinas tragamonedas o **Multi-Armed Bandit**.

El propósito es observar cómo pueden estimarse las recompensas esperadas de varias acciones cuando los parámetros reales no son conocidos por el agente.

La pregunta guía es:

> Si no conocemos la recompensa media de cada máquina, ¿cómo podemos estimar cuál máquina conviene elegir?

## 2. Descripción del problema

Se consideran tres máquinas. La recompensa de cada máquina sigue una distribución normal con los siguientes parámetros:

```text
A1: media real = 1.0, desviación estándar real = 0.5
A2: media real = 2.0, desviación estándar real = 0.5
A3: media real = 1.5, desviación estándar real = 1.5
```

Formalmente:

```text
A1 ~ Normal(1.0, 0.5)
A2 ~ Normal(2.0, 0.5)
A3 ~ Normal(1.5, 1.5)
```

En este reto se utilizará la convención:

```text
Normal(media, desviación estándar)
```

La máquina `A3` tiene una desviación estándar considerablemente mayor. Por tanto, puede generar recompensas altas, pero también presenta mayor variabilidad y una mayor probabilidad de producir recompensas bajas.

## 3. Objetivos de aprendizaje

Al finalizar el reto, el estudiante deberá estar en capacidad de:

- Representar recompensas mediante distribuciones normales.
- Construir una función de simulación reproducible.
- Generar muestras aleatorias.
- Calcular estadísticos descriptivos.
- Comparar parámetros reales con estimaciones muestrales.
- Visualizar distribuciones de recompensas.
- Interpretar la relación entre recompensa esperada y riesgo.
- Documentar un análisis técnico en un notebook.
- Utilizar Git, Docker y Pull Requests para entregar el trabajo.

## 4. Herramientas

El reto debe desarrollarse utilizando:

- Python 3.11.
- NumPy.
- Pandas.
- Matplotlib.
- Jupyter Notebook dentro de Visual Studio Code.
- Docker mediante el Dev Container del curso.
- Git y GitHub.

## 5. Archivo de entrega

El trabajo debe realizarse en:

```text
challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb
```

Reemplaza `apellido_nombre` por tus datos.

Ejemplo:

```text
reto_01_perez_ana.ipynb
```

No utilices espacios, tildes ni caracteres especiales en el nombre del archivo.

También debes exportar el notebook a HTML y guardarlo en:

```text
challenges/challenge_01_bandits/submission/exports/
```

Ejemplo:

```text
challenges/challenge_01_bandits/submission/exports/reto_01_perez_ana.html
```

## 6. Actividades obligatorias

### Parte 1 — Portada y preparación

Incluye una portada en Markdown con:

- Nombre del curso.
- Título del reto.
- Nombres completos de los integrantes.
- Correos institucionales.
- Fecha de entrega.
- Objetivo del notebook.

Importa, como mínimo:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
```

Define una semilla para hacer reproducibles los resultados:

```python
SEED = 42
rng = np.random.default_rng(SEED)
```

### Parte 2 — Definición de las máquinas

Representa las máquinas utilizando:

```python
MACHINES = {
    "A1": {"mean": 1.0, "std": 0.5},
    "A2": {"mean": 2.0, "std": 0.5},
    "A3": {"mean": 1.5, "std": 1.5},
}
```

Explica brevemente:

- Qué representa `mean`.
- Qué representa `std`.
- Por qué dos máquinas con medias similares pueden producir resultados diferentes.

### Parte 3 — Función de recompensa

Construye una función:

```python
reward(arm)
```

La función debe:

1. Recibir el nombre de una máquina: `"A1"`, `"A2"` o `"A3"`.
2. Consultar sus parámetros.
3. Generar una recompensa mediante una distribución normal.
4. Retornar la recompensa como un número decimal.
5. Generar un error claro si la máquina no existe.

Ejemplo:

```python
reward("A1")
```

Prueba la función con las tres máquinas.

### Parte 4 — Simulación

Simula exactamente:

```text
1.000 recompensas por máquina
```

Se recomienda construir un DataFrame con esta estructura:

```text
machine | sample | reward
A1      | 1      | ...
A1      | 2      | ...
...
A3      | 1000   | ...
```

El resultado completo debe contener:

```text
3.000 registros
```

Incluye verificaciones explícitas sobre:

- Número de observaciones por máquina.
- Total de observaciones.
- Presencia de valores faltantes.
- Tipo de los datos.

### Parte 5 — Estadísticos descriptivos

Para cada máquina calcula:

- Media muestral.
- Desviación estándar muestral.
- Varianza muestral.
- Recompensa mínima.
- Recompensa máxima.

Utiliza la convención muestral:

```python
std(ddof=1)
var(ddof=1)
```

Construye una tabla con las siguientes columnas:

```text
Máquina
Media real
Media estimada
Error absoluto de la media
Desviación real
Desviación estimada
Varianza estimada
Mínimo
Máximo
```

El error absoluto de la media se calcula como:

```text
|media estimada - media real|
```

### Parte 6 — Visualizaciones

Incluye una gráfica individual por máquina.

Cada gráfica debe mostrar:

- Histograma de recompensas.
- Título.
- Etiqueta del eje horizontal.
- Etiqueta del eje vertical.
- Línea vertical con la media real.
- Línea vertical con la media estimada.
- Leyenda.

Utiliza los mismos límites del eje horizontal en las tres gráficas cuando sea posible, para facilitar la comparación.

Opcionalmente, puedes incluir una gráfica adicional que compare las tres máquinas.

### Parte 7 — Interpretación

Responde en Markdown:

1. ¿Cuál máquina tuvo la mayor recompensa media estimada?
2. ¿La máquina con mayor media estimada coincide con la de mayor media real?
3. ¿Cuál máquina presentó mayor desviación y varianza?
4. ¿Por qué `A3` puede considerarse más riesgosa?
5. ¿Una recompensa ocasionalmente alta implica que una máquina sea la mejor?
6. ¿Qué puede ocurrir si se estima la media utilizando pocas observaciones?
7. Si las medias reales fueran desconocidas, ¿qué información utilizarías para decidir cuál máquina elegir?
8. ¿Cómo cambiarían tus conclusiones si solo se observaran 10 recompensas por máquina?

Las respuestas deben estar sustentadas en los resultados obtenidos.

### Parte 8 — Experimento adicional

Repite la estimación de las medias utilizando:

```text
10, 50, 100 y 1.000 observaciones
```

Construye una tabla que compare la media estimada de cada máquina para cada tamaño de muestra.

Analiza:

- Cómo cambia la estimación al aumentar el número de observaciones.
- En qué máquina parece haber mayor inestabilidad.
- Por qué una mayor variabilidad dificulta la estimación.

### Parte 9 — Uso de inteligencia artificial

Incluye una sección titulada:

```text
Uso de inteligencia artificial
```

Documenta:

- Herramienta utilizada.
- Prompts o preguntas principales.
- Recomendaciones recibidas.
- Cambios realizados manualmente.
- Recomendaciones que decidiste no utilizar.
- Cómo verificaste que las sugerencias fueran correctas.

No es necesario copiar conversaciones completas.

Ejemplo:

```text
Herramienta:
Microsoft Copilot.

Pregunta:
¿Cómo puedo agregar una línea vertical con la media a un histograma
de Matplotlib?

Sugerencia recibida:
Usar ax.axvline(...).

Ajuste manual:
Se modificaron los colores y se agregaron líneas separadas para la
media real y la media estimada.

Validación:
Se compararon los valores de las líneas con la tabla estadística.
```

La responsabilidad sobre el código, el análisis y las conclusiones continúa siendo del estudiante.

### Parte 10 — Conclusiones

Incluye entre tres y cinco conclusiones.

Las conclusiones deben responder como mínimo:

- Cuál máquina presentó la mayor recompensa media.
- Cuál máquina presentó mayor riesgo o variabilidad.
- Qué diferencia existe entre una recompensa individual y una recompensa esperada.
- Cómo influye el tamaño de la muestra.
- Qué aprendiste acerca de seleccionar acciones cuando sus parámetros son desconocidos.

## 7. Restricciones

No debes modificar:

```text
challenges/challenge_01_bandits/starter_code/
challenges/challenge_01_bandits/tests/
.github/workflows/
docker/
docker-compose.yml
```

No debes:

- Usar números generados manualmente como si fueran resultados.
- Eliminar resultados desfavorables.
- Cambiar los parámetros reales de las máquinas.
- Subir datasets o archivos innecesarios.
- Entregar un notebook con errores de ejecución.
- Entregar celdas importantes sin ejecutar.
- Incluir contraseñas, tokens o información sensible.

## 8. Verificación local

Ejecuta:

```bash
pytest challenges/challenge_01_bandits/tests -v
```

Después ejecuta todas las celdas del notebook:

```text
Restart Kernel and Run All Cells
```

Confirma que ninguna celda produzca errores.

## 9. Exportación a HTML

Reemplaza el nombre del archivo por el correspondiente:

```bash
jupyter nbconvert \
  --to html \
  challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb \
  --output-dir challenges/challenge_01_bandits/submission/exports
```

Verifica que el archivo HTML haya sido creado.

## 10. Entrega mediante Git

Actualiza el repositorio y crea una rama:

```bash
git switch main
git pull origin main
git switch -c challenge-01-nombre-apellido
```

Agrega únicamente el notebook y su exportación:

```bash
git add challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb
git add challenges/challenge_01_bandits/submission/exports/reto_01_apellido_nombre.html
```

Crea el commit:

```bash
git commit -m "feat: entregar reto 01 de bandits"
```

Publica la rama:

```bash
git push -u origin challenge-01-nombre-apellido
```

Después crea un Pull Request hacia `main`.

## 11. Criterios de evaluación

### Implementación y reproducibilidad — 25 %

- Función `reward(arm)` correcta.
- Uso adecuado de semillas.
- Simulación de 1.000 recompensas por máquina.
- Código ejecutable desde el inicio.

### Análisis estadístico — 25 %

- Estadísticos correctos.
- Tabla comparativa completa.
- Comparación entre valores reales y estimados.
- Experimento con diferentes tamaños de muestra.

### Visualización e interpretación — 25 %

- Una gráfica por máquina.
- Gráficas legibles y correctamente etiquetadas.
- Interpretación de media, desviación y varianza.
- Análisis del riesgo de `A3`.

### Documentación y comunicación — 15 %

- Portada.
- Organización del notebook.
- Explicaciones en Markdown.
- Conclusiones sustentadas en resultados.

### Uso responsable de IA — 10 %

- Prompts principales documentados.
- Ajustes manuales explicados.
- Validación de las sugerencias.
- Reflexión sobre el uso de la herramienta.

## 12. Lista de verificación

Antes de crear el Pull Request:

- [ ] Cambié el nombre del notebook.
- [ ] Incluí nombres y correos.
- [ ] Definí una semilla.
- [ ] Implementé `reward(arm)`.
- [ ] Generé 1.000 recompensas por máquina.
- [ ] Construí la tabla comparativa.
- [ ] Incluí tres gráficas individuales.
- [ ] Comparé parámetros reales y estimados.
- [ ] Analicé diferentes tamaños de muestra.
- [ ] Expliqué por qué `A3` es más riesgosa.
- [ ] Documenté el uso de IA.
- [ ] Incluí conclusiones.
- [ ] Ejecuté todas las celdas.
- [ ] No hay errores de ejecución.
- [ ] Exporté el notebook a HTML.
- [ ] Ejecuté las pruebas.
- [ ] Revisé `git status`.
