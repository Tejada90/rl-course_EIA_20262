# Guía de inicio para estudiantes

Esta guía presenta el recorrido completo para preparar el entorno, comprobar
Docker, desarrollar el Reto 1 y entregar el trabajo mediante GitHub.

## 1. Qué se necesita

Antes de comenzar, instala:

1. [Git](https://git-scm.com/downloads).
2. [Docker Desktop](https://www.docker.com/products/docker-desktop/).
3. [Visual Studio Code](https://code.visualstudio.com/).
4. La extensión **Dev Containers** de Microsoft para Visual Studio Code.

Abre Docker Desktop y espera hasta que indique que el motor está listo.

## 2. Clonar el repositorio

Este paso se realiza una sola vez. Abre PowerShell, Terminal o Git Bash y
ejecuta:

```bash
git clone https://github.com/Tejada90/rl-course_EIA_20262.git
cd rl-course_EIA_20262
code .
```

Si `code .` no funciona, abre Visual Studio Code, selecciona **File > Open
Folder** y elige la carpeta `rl-course_EIA_20262`.

No descargues el repositorio como ZIP: un ZIP no conserva la información de
Git necesaria para crear ramas y entregar el trabajo.

## 3. Abrir el entorno del curso

Con el repositorio abierto en Visual Studio Code:

1. Presiona `Ctrl + Shift + P`.
2. Busca `Dev Containers: Reopen in Container`.
3. Selecciona el comando y espera a que termine la construcción.
4. Comprueba que la esquina inferior izquierda muestre
   `Dev Container: Curso RL EIA 2026-2`.
5. Abre una terminal con **Terminal > New Terminal**.

La terminal debe encontrarse en `/workspace`:

```bash
pwd
python --version
git status
```

El resultado de Python debe comenzar con `Python 3.11`. Los archivos de
`/workspace` están vinculados con la carpeta local y no desaparecen cuando se
detiene o reconstruye el contenedor.

### Alternativa sin Dev Containers

Desde una terminal en la raíz del repositorio:

```bash
docker compose up -d --build
docker compose exec rl-course bash
```

Los comandos restantes de esta guía se ejecutan dentro del contenedor.

## 4. Configurar Git

Configura tu identidad con el nombre y correo que usarás en GitHub:

```bash
git config --global user.name "Nombre Apellido"
git config --global user.email "correo@eia.edu.co"
git config --global --list
```

No compartas contraseñas, tokens ni llaves privadas en el repositorio.

## 5. Ejecutar el ejemplo inicial

Antes de modificar el reto, ejecuta:

```bash
python examples/docker_quickstart.py
```

El programa debe:

- Mostrar las versiones de NumPy, Gymnasium y PyTorch.
- Indicar que PyTorch utiliza CPU.
- Simular 1.000 recompensas para cada máquina.
- Mostrar una media estimada para `A1`, `A2` y `A3`.

Después verifica las pruebas existentes:

```bash
pytest -q
```

El entorno está listo si el ejemplo termina sin errores y todas las pruebas
pasan. Consulta `examples/README.md` para conocer los comandos equivalentes de
Docker Compose.

## 6. Preparar una entrega del Reto 1

No desarrolles directamente sobre `main`. Primero confirma que no tengas
cambios sin guardar:

```bash
git status
```

Actualiza la rama principal:

```bash
git switch main
git pull origin main
```

Crea una rama personal. Usa minúsculas, guiones y evita espacios, tildes o
caracteres especiales:

```bash
git switch -c challenge-01-nombre-apellido
```

Ejemplo:

```bash
git switch -c challenge-01-ana-perez
```

Confirma que no estás en `main`:

```bash
git branch --show-current
```

## 7. Preparar el notebook

La plantilla se encuentra en:

```text
challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb
```

Crea una copia y cámbiale el nombre con el formato
`reto_01_apellido_nombre.ipynb`. Por ejemplo:

```text
reto_01_perez_ana.ipynb
```

No uses nombres como `final.ipynb`, espacios, mayúsculas, tildes o la letra
`ñ`. Conserva la plantilla original y trabaja únicamente en tu copia.

Abre el notebook en Visual Studio Code y selecciona el kernel de Python del
contenedor. El intérprete esperado es `/usr/local/bin/python`.

## 8. Lineamientos del Reto 1

El enunciado completo y los criterios de evaluación están en
`challenges/challenge_01_bandits/README.md`. El notebook debe incluir, como
mínimo, las siguientes secciones.

### Portada y reproducibilidad

Incluye nombres, correos institucionales, fecha, título y objetivo. Define una
semilla y usa un generador de NumPy:

```python
SEED = 42
rng = np.random.default_rng(SEED)
```

### Máquinas y función de recompensa

Representa exactamente las tres máquinas del enunciado e implementa
`reward(arm)`. La función debe producir un `float` y generar un error claro si
la máquina no existe.

### Simulación

Genera exactamente 1.000 recompensas por máquina y construye un conjunto de
3.000 registros. Comprueba cantidades, tipos y valores faltantes.

### Estadísticos

Calcula media, desviación estándar, varianza, mínimo y máximo. Para desviación
y varianza muestral utiliza `ddof=1`. Compara los valores estimados con los
parámetros reales y calcula el error absoluto de cada media.

### Visualizaciones

Incluye un histograma individual para cada máquina, con títulos, ejes, leyenda
y líneas para las medias real y estimada. Usa escalas comparables.

### Interpretación y experimento adicional

Responde las preguntas del enunciado usando evidencia de tablas y gráficas.
Compara estimaciones con 10, 50, 100 y 1.000 observaciones y explica el efecto
del tamaño de muestra y la variabilidad.

### Uso de inteligencia artificial y conclusiones

Documenta la herramienta, preguntas principales, sugerencias, cambios
manuales y método de validación. Incluye entre tres y cinco conclusiones
sustentadas en los resultados.

### Archivos restringidos

No modifiques:

```text
challenges/challenge_01_bandits/starter_code/
challenges/challenge_01_bandits/tests/
.github/workflows/
docker/
docker-compose.yml
```

## 9. Validar el trabajo

En el notebook selecciona **Restart Kernel and Run All Cells**. Confirma que
las celdas se ejecuten en orden, que las gráficas aparezcan y que no existan
errores.

Ejecuta las pruebas:

```bash
pytest challenges/challenge_01_bandits/tests -v
```

Revisa los archivos modificados:

```bash
git status
git diff --stat
```

No continúes si aparecen archivos de pruebas, Docker o configuración entre tus
cambios.

## 10. Exportar el notebook

Reemplaza el nombre del ejemplo por el de tu entrega:

```bash
jupyter nbconvert \
  --to html \
  challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb \
  --output-dir challenges/challenge_01_bandits/submission/exports
```

Comprueba que el HTML abra correctamente y muestre código, resultados, tablas
y gráficas. La estructura esperada es:

```text
submission/
├── README.md
├── reto_01_apellido_nombre.ipynb
└── exports/
    └── reto_01_apellido_nombre.html
```

## 11. Crear el commit

Agrega únicamente el notebook personal y su HTML:

```bash
git add challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb
git add challenges/challenge_01_bandits/submission/exports/reto_01_apellido_nombre.html
git status
```

Revisa la lista antes de crear el commit:

```bash
git commit -m "feat: entregar reto 01 de bandits"
```

## 12. Publicar y crear el Pull Request

Publica tu rama:

```bash
git push -u origin challenge-01-nombre-apellido
```

En GitHub:

1. Abre el repositorio.
2. Selecciona **Compare & pull request**.
3. Confirma que la rama base sea `main`.
4. Confirma que la rama de comparación sea tu rama `challenge-01-...`.
5. Completa toda la plantilla del Pull Request.
6. Incluye el resultado de `pytest`.
7. Crea el Pull Request.
8. Espera a que GitHub Actions termine.

No intentes hacer push directamente a `main`. Las reglas del repositorio
exigen un Pull Request y pruebas automáticas exitosas.

Si un check falla, abre sus detalles, corrige el trabajo en la misma rama,
crea otro commit y ejecuta `git push`. El Pull Request se actualizará
automáticamente. No crees otro Pull Request para la misma entrega.

## 13. Atender revisión y finalizar

Responde los comentarios del profesor y publica las correcciones en la misma
rama. La entrega termina cuando:

- El Pull Request contiene únicamente los archivos autorizados.
- Todas las pruebas automáticas pasan.
- No existen conversaciones de revisión pendientes.
- El profesor acepta o fusiona el Pull Request según las reglas del curso.

No elimines la rama antes de que termine la revisión.

## 14. Lista final de verificación

- [ ] Trabajé dentro del Dev Container.
- [ ] Actualicé `main` antes de crear mi rama.
- [ ] Confirmé que no estoy trabajando directamente en `main`.
- [ ] Renombré mi copia del notebook correctamente.
- [ ] Ejecuté todas las celdas desde el inicio.
- [ ] Generé 1.000 recompensas por máquina.
- [ ] Incluí tablas, tres gráficas e interpretación.
- [ ] Realicé el experimento con diferentes tamaños de muestra.
- [ ] Documenté el uso de inteligencia artificial.
- [ ] Incluí conclusiones.
- [ ] Ejecuté `pytest` y todas las pruebas pasaron.
- [ ] Exporté el notebook a HTML y lo revisé.
- [ ] Agregué únicamente el notebook y el HTML.
- [ ] Creé el Pull Request hacia `main`.
- [ ] Revisé el resultado de GitHub Actions.

## 15. Solución de problemas

Si Docker no responde, confirma que Docker Desktop esté abierto:

```bash
docker info
```

Si cambian las dependencias o la imagen, ejecuta **Dev Containers: Rebuild
Container**. Para otros problemas consulta:

- `docs/setup.md`
- `docs/docker.md`
- `docs/troubleshooting.md`
- `docs/workflow.md`
