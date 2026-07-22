# Ejemplo de uso del entorno Docker

Este ejemplo permite confirmar que Docker, Python y las principales
dependencias del curso funcionan antes de comenzar un reto.

## Opción 1: Visual Studio Code y Dev Containers

1. Abre Docker Desktop.
2. Abre la raíz del repositorio en Visual Studio Code.
3. Presiona `Ctrl + Shift + P`.
4. Ejecuta `Dev Containers: Reopen in Container`.
5. Abre una terminal integrada y ejecuta:

```bash
python examples/docker_quickstart.py
```

La terminal se encuentra en `/workspace`, que corresponde a la carpeta del
repositorio en el computador.

## Opción 2: Docker Compose desde una terminal

Desde la raíz del repositorio, construye e inicia el entorno:

```bash
docker compose up -d --build
```

Ejecuta el ejemplo dentro del contenedor:

```bash
docker compose exec rl-course python examples/docker_quickstart.py
```

Ejecuta las pruebas:

```bash
docker compose exec rl-course pytest -q
```

Al terminar, detén el entorno:

```bash
docker compose down
```

## Qué demuestra el ejemplo

El programa:

- Muestra las versiones de NumPy, Gymnasium y PyTorch.
- Confirma que se usa la distribución de PyTorch para CPU.
- Importa código del repositorio mediante `PYTHONPATH=/workspace`.
- Genera 1.000 recompensas reproducibles para cada máquina.
- Calcula sus medias con tensores de PyTorch.

Los archivos editados dentro de `/workspace` se guardan directamente en la
carpeta local del repositorio y no desaparecen al detener el contenedor.
