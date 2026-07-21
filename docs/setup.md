# Configuración del entorno

Esta guía explica cómo instalar y configurar las herramientas necesarias para el curso.

## Herramientas requeridas

Debes instalar:

1. Git.
2. Docker Desktop.
3. Visual Studio Code.
4. La extensión Dev Containers de Visual Studio Code.

## 1. Instalar Git

Descarga Git desde:

https://git-scm.com/downloads

Después de instalarlo, abre una terminal y ejecuta:

```bash
git --version
```

El resultado debe ser similar a:

```text
git version 2.x.x
```

### Configurar tu identidad

Reemplaza los datos del ejemplo por tu nombre y correo:

```bash
git config --global user.name "Nombre Apellido"
```

```bash
git config --global user.email "correo@ejemplo.com"
```

Verifica la configuración:

```bash
git config --global --list
```

Es recomendable utilizar el mismo correo asociado a tu cuenta de GitHub.

## 2. Instalar Docker Desktop

Descarga Docker Desktop desde:

https://www.docker.com/products/docker-desktop/

Después de instalarlo:

1. Reinicia el computador si el instalador lo solicita.
2. Abre Docker Desktop.
3. Espera hasta que Docker indique que está listo.
4. Abre una terminal.

Ejecuta:

```bash
docker --version
```

Después ejecuta:

```bash
docker compose version
```

Ambos comandos deben mostrar una versión instalada.

## 3. Instalar Visual Studio Code

Descarga Visual Studio Code desde:

https://code.visualstudio.com/

## 4. Instalar Dev Containers

En Visual Studio Code:

1. Abre **Extensions**.
2. Busca `Dev Containers`.
3. Instala la extensión publicada por Microsoft.

Su identificador es:

```text
ms-vscode-remote.remote-containers
```

También se recomiendan:

- Python.
- Pylance.
- Jupyter.
- Docker.
- GitLens.

Visual Studio Code te ofrecerá instalarlas automáticamente al abrir este repositorio.

## 5. Clonar el repositorio

Abre una terminal y ejecuta:

```bash
git clone https://github.com/Tejada90/rl-course_EIA_20262.git
```

Entra a la carpeta:

```bash
cd rl-course_EIA_20262
```

## 6. Abrir Visual Studio Code

Ejecuta:

```bash
code .
```

Si el comando no está disponible:

1. Abre Visual Studio Code.
2. Selecciona **File**.
3. Selecciona **Open Folder**.
4. Busca y selecciona `rl-course_EIA_20262`.

## 7. Abrir el proyecto dentro de Docker

Antes de continuar, confirma que Docker Desktop esté abierto.

En Visual Studio Code:

1. Presiona `Ctrl + Shift + P`.
2. Escribe `Dev Containers`.
3. Selecciona:

```text
Dev Containers: Reopen in Container
```

Visual Studio Code comenzará a construir el entorno.

La primera construcción puede tardar varios minutos porque Docker debe:

- Descargar Python 3.11.
- Instalar Git.
- Instalar las dependencias.
- Configurar las extensiones.

Las siguientes aperturas serán más rápidas.

## 8. Confirmar que estás dentro del contenedor

Observa la esquina inferior izquierda de Visual Studio Code.

Debe aparecer un indicador similar a:

```text
Dev Container: Curso RL EIA 2026-2
```

## 9. Abrir una terminal integrada

Selecciona:

```text
Terminal > New Terminal
```

La terminal debe abrirse en:

```text
/workspace
```

Verifica la ruta:

```bash
pwd
```

## 10. Verificar Python

```bash
python --version
```

El resultado esperado comienza por:

```text
Python 3.11
```

## 11. Verificar las dependencias

Ejecuta:

```bash
python -c "import numpy, gymnasium, torch; print('Entorno configurado correctamente')"
```

El resultado esperado es:

```text
Entorno configurado correctamente
```

## 12. Ejecutar las pruebas

```bash
pytest
```

También puedes ejecutar:

```bash
pytest -v
```

Para ejecutar únicamente las pruebas del primer reto:

```bash
pytest challenges/challenge_01_bandits/tests -v
```

## 13. Cerrar el entorno

En Visual Studio Code:

1. Presiona `Ctrl + Shift + P`.
2. Selecciona:

```text
Dev Containers: Reopen Folder Locally
```

Después puedes detener los contenedores:

```bash
docker compose down
```

## 14. Reconstruir el entorno

Si cambia el archivo `requirements.txt` o el `Dockerfile`:

1. Presiona `Ctrl + Shift + P`.
2. Selecciona:

```text
Dev Containers: Rebuild Container
```

## Resultado esperado

Al finalizar debes poder ejecutar:

```bash
python --version
pytest
git status
```

sin recibir errores.
``
