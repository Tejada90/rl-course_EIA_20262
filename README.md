# Curso de Aprendizaje por Refuerzo — Universidad EIA

Repositorio oficial del curso de **Aprendizaje por Refuerzo** de la Universidad EIA, correspondiente al segundo semestre de 2026.

## Objetivos del repositorio

Este repositorio permite:

- Consultar el material y los retos del curso.
- Desarrollar soluciones con Python.
- Trabajar con un entorno reproducible basado en Docker.
- Utilizar Visual Studio Code como entorno de desarrollo.
- Ejecutar pruebas automáticas con `pytest`.
- Entregar los retos mediante ramas y Pull Requests.
- Recibir validación automática mediante GitHub Actions.

## Tecnologías

- Python 3.11
- Docker y Docker Compose
- Visual Studio Code
- Dev Containers
- Git y GitHub
- NumPy
- Gymnasium
- PyTorch
- Pytest
- JupyterLab

## Requisitos

Antes de comenzar debes instalar:

1. https://git-scm.com/downloads
2. https://www.docker.com/products/docker-desktop/
3. https://code.visualstudio.com/
4. La extensión **Dev Containers** de Visual Studio Code

Consulta la guía detallada:

docs/setup.md

## Inicio rápido

### 1. Clonar el repositorio

```bash
git clone https://github.com/Tejada90/rl-course_EIA_20262.git
```

### 2. Entrar al repositorio

```bash
cd rl-course_EIA_20262
```

### 3. Abrir Visual Studio Code

```bash
code .
```

Si el comando `code` no está disponible, abre Visual Studio Code manualmente y selecciona:

```text
File > Open Folder
```

### 4. Abrir el proyecto dentro de Docker

En Visual Studio Code:

1. Presiona `Ctrl + Shift + P`.
2. Escribe `Dev Containers`.
3. Selecciona:

```text
Dev Containers: Reopen in Container
```

La primera construcción puede tardar varios minutos.

La imagen instala la versión de PyTorch para CPU. Esto evita descargar
componentes CUDA innecesarios y hace que el entorno sea más ligero y
reproducible en los equipos del curso.

### 5. Verificar el entorno

Abre una terminal integrada en Visual Studio Code y ejecuta:

```bash
python --version
```

Después ejecuta:

```bash
python -c "import numpy, gymnasium, torch; print('Entorno configurado correctamente')"
```

### 6. Ejecutar las pruebas

```bash
pytest
```

Para ver más detalles:

```bash
pytest -v
```

### 7. Ejecutar el ejemplo de Docker

Para comprobar el entorno y ejecutar una simulación pequeña:

```bash
python examples/docker_quickstart.py
```

Consulta la guía completa en `examples/README.md`.

## Retos

| Reto | Tema | Estado |
|---|---|---|
| 01 | Multi-Armed Bandits | Disponible |
| 02 | Comparación de algoritmos bandit | Disponible |
| 03 | Q-Learning | Próximamente |
| 04 | Deep Q-Network | Próximamente |
| 05 | Policy Gradient | Próximamente |
| 06 | PPO | Próximamente |

El primer reto se encuentra en:

```text
challenges/challenge_01_bandits/
```

Consulta su enunciado:

challenges/challenge_01_bandits/README.md

El segundo reto se encuentra en:

```text
challenges/challenge_02_bandit_algorithms/
```

Consulta su enunciado:

challenges/challenge_02_bandit_algorithms/README.md

## Flujo de entrega

Cada entrega debe seguir este flujo:

```text
Actualizar main
      ↓
Crear una rama
      ↓
Resolver el reto
      ↓
Ejecutar pytest
      ↓
Crear un commit
      ↓
Hacer push
      ↓
Crear un Pull Request
```

Consulta las instrucciones completas:

docs/workflow.md

## Documentación

- docs/guia_inicio_estudiantes.md
- docs/setup.md
- docs/docker.md
- docs/workflow.md
- docs/troubleshooting.md

## Comandos frecuentes

### Ejecutar todas las pruebas

```bash
pytest
```

### Ejecutar las pruebas del primer reto

```bash
pytest challenges/challenge_01_bandits/tests -v
```

### Revisar cambios de Git

```bash
git status
```

### Descargar actualizaciones

```bash
git pull origin main
```

### Crear una rama

```bash
git switch -c challenge-01-nombre-apellido
```

### Publicar una rama

```bash
git push -u origin challenge-01-nombre-apellido
```

## Reglas generales

1. No desarrollar directamente sobre la rama `main`.
2. Crear una rama independiente para cada reto.
3. Modificar únicamente los archivos autorizados en cada reto.
4. Ejecutar las pruebas antes de hacer push.
5. No modificar los archivos de evaluación.
6. No subir modelos, checkpoints, conjuntos de datos pesados o archivos generados.
7. Cada entrega debe realizarse mediante un Pull Request.

## Autor

Material preparado para el curso de Aprendizaje por Refuerzo de la Universidad EIA.

## Licencia

Este repositorio se distribuye bajo la licencia MIT. Consulta el archivo LICENSE.
