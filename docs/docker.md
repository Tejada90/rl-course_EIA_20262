# Guía básica de Docker

Docker permite utilizar el mismo entorno de desarrollo en todos los computadores.

## Conceptos principales

### Imagen

Una imagen es una plantilla que contiene:

- Sistema operativo base.
- Python.
- Git.
- Dependencias del curso.

### Contenedor

Un contenedor es una instancia en ejecución de una imagen.

### Dockerfile

El archivo `docker/Dockerfile` describe cómo construir la imagen.

### Docker Compose

El archivo `docker-compose.yml` describe cómo ejecutar el contenedor y conectar el repositorio con él.

### Dev Container

El archivo `.devcontainer/devcontainer.json` permite que Visual Studio Code abra el repositorio dentro del contenedor.

## Forma recomendada de usar Docker

1. Abre Docker Desktop.
2. Abre el repositorio en Visual Studio Code.
3. Presiona `Ctrl + Shift + P`.
4. Selecciona:

```text
Dev Containers: Reopen in Container
```

## Comandos de Docker

Los siguientes comandos se ejecutan desde la raíz del repositorio.

### Construir la imagen

```bash
docker compose build
```

### Iniciar el contenedor

```bash
docker compose up -d
```

La opción `-d` ejecuta el contenedor en segundo plano.

### Ver el estado

```bash
docker compose ps
```

### Entrar manualmente al contenedor

```bash
docker compose exec rl-course bash
```

### Consultar los registros

```bash
docker compose logs
```

### Detener el entorno

```bash
docker compose down
```

### Reconstruir sin utilizar caché

```bash
docker compose build --no-cache
```

## Relación entre el computador y Docker

El repositorio de tu computador se monta en:

```text
/workspace
```

dentro del contenedor.

La configuración utilizada es:

```yaml
volumes:
  - .:/workspace
```

Esto significa que:

- Los archivos editados en Visual Studio Code se guardan en tu computador.
- Python se ejecuta dentro de Docker.
- Git puede detectar y publicar los cambios.
- Los archivos no desaparecen al detener el contenedor.

## Comprobar el entorno

Dentro del contenedor:

```bash
python --version
```

Comprobar las dependencias:

```bash
python -c "import numpy, gymnasium, torch; print('Dependencias disponibles')"
```

Ejecutar pruebas:

```bash
pytest
```

## Agregar una nueva dependencia

No instales dependencias solamente con `pip install` dentro del contenedor, porque desaparecerán al reconstruirlo.

El procedimiento correcto es:

1. Agregar la dependencia a `requirements.txt`.
2. Reconstruir el contenedor.
3. Verificar que las pruebas funcionen.

Para reconstruirlo desde Visual Studio Code:

```text
Dev Containers: Rebuild Container
```

## Problemas comunes

### Docker no responde

Confirma que Docker Desktop esté abierto.

Ejecuta:

```bash
docker info
```

### El contenedor no aparece

Ejecuta:

```bash
docker compose ps
```

### Revisar errores de construcción

```bash
docker compose build --no-cache
```

### Detener y volver a iniciar

```bash
docker compose down
docker compose up -d
```

## Recomendación

No utilices comandos globales de limpieza de Docker sin comprender sus efectos. Algunos comandos pueden eliminar imágenes o contenedores pertenecientes a otros proyectos.
