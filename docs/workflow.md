# Flujo de trabajo con Git y GitHub

Esta guía explica cómo desarrollar y entregar los retos del curso de Aprendizaje por Refuerzo utilizando:

- Visual Studio Code.
- Docker y Dev Containers.
- Git.
- GitHub.
- Ramas.
- Commits.
- Push.
- Pull Requests.
- GitHub Actions.

Cada entrega debe realizarse desde una rama independiente. No se permite trabajar ni entregar directamente sobre la rama `main`.

---

# 1. Flujo general de trabajo

Cada reto seguirá este proceso:

```text
Abrir Docker Desktop
        ↓
Abrir el repositorio en Visual Studio Code
        ↓
Abrir el proyecto dentro del Dev Container
        ↓
Actualizar la rama main
        ↓
Crear una rama para el reto
        ↓
Desarrollar el notebook
        ↓
Ejecutar todas las celdas
        ↓
Ejecutar las pruebas
        ↓
Exportar el notebook a HTML
        ↓
Revisar los archivos modificados
        ↓
Crear un commit
        ↓
Hacer push de la rama
        ↓
Crear un Pull Request
        ↓
Revisar GitHub Actions
        ↓
Atender comentarios del profesor
```

---

# 2. Antes de comenzar

Debes tener instaladas las siguientes herramientas:

1. Git.
2. Docker Desktop.
3. Visual Studio Code.
4. La extensión Dev Containers para Visual Studio Code.

Consulta la guía de instalación:

```text
docs/setup.md
```

También debes haber aceptado la invitación como colaborador del repositorio, si el profesor está utilizando un repositorio compartido.

---

# 3. Clonar el repositorio por primera vez

Este procedimiento solo es necesario la primera vez que trabajas con el repositorio.

Abre una terminal en tu computador y ejecuta:

```bash
git clone https://github.com/Tejada90/rl-course_EIA_20262.git
```

Entra a la carpeta descargada:

```bash
cd rl-course_EIA_20262
```

Abre el repositorio en Visual Studio Code:

```bash
code .
```

Si el comando `code` no está disponible:

1. Abre Visual Studio Code manualmente.
2. Selecciona **File**.
3. Selecciona **Open Folder**.
4. Busca la carpeta `rl-course_EIA_20262`.
5. Presiona **Select Folder**.

---

# 4. Abrir el proyecto dentro de Docker

Antes de abrir el Dev Container, inicia Docker Desktop.

Espera hasta que Docker Desktop indique que el motor de Docker está funcionando.

En Visual Studio Code:

1. Presiona `Ctrl + Shift + P`.
2. Escribe:

```text
Dev Containers
```

3. Selecciona:

```text
Dev Containers: Reopen in Container
```

La primera construcción puede tardar varios minutos.

Docker deberá:

- Descargar la imagen base de Python.
- Instalar Git.
- Instalar las dependencias del curso.
- Configurar las extensiones de Visual Studio Code.
- Abrir el repositorio en `/workspace`.

Cuando termine, la esquina inferior izquierda de Visual Studio Code debe mostrar algo similar a:

```text
Dev Container: Curso RL EIA 2026-2
```

---

# 5. Abrir una terminal dentro del contenedor

En Visual Studio Code selecciona:

```text
Terminal > New Terminal
```

Comprueba la ubicación actual:

```bash
pwd
```

El resultado esperado es:

```text
/workspace
```

Verifica Python:

```bash
python --version
```

El resultado debe comenzar por:

```text
Python 3.11
```

Verifica Git:

```bash
git --version
```

Revisa el estado actual del repositorio:

```bash
git status
```

---

# 6. Configurar la identidad de Git

Este procedimiento generalmente solo es necesario una vez.

Configura tu nombre:

```bash
git config --global user.name "Nombre Apellido"
```

Configura tu correo:

```bash
git config --global user.email "correo@eia.edu.co"
```

Utiliza preferiblemente el mismo correo asociado con tu cuenta de GitHub.

Verifica la configuración:

```bash
git config --global --list
```

Si Git muestra una advertencia relacionada con un directorio inseguro, ejecuta:

```bash
git config --global --add safe.directory /workspace
```

---

# 7. Actualizar la rama principal

Antes de comenzar un reto, debes actualizar la rama `main`.

Primero revisa si tienes archivos modificados:

```bash
git status
```

Si el repositorio está limpio, cambia a `main`:

```bash
git switch main
```

Descarga los cambios más recientes:

```bash
git pull origin main
```

El resultado puede mostrar:

```text
Already up to date.
```

Esto significa que ya tienes la última versión.

También puede mostrar una lista de archivos actualizados. En ese caso, Git descargó nuevo material publicado por el profesor.

---

# 8. Crear una rama para el Reto 1

No debes desarrollar directamente sobre `main`.

Para el Reto 1 utiliza esta convención:

```text
challenge-01-nombre-apellido
```

Ejemplo:

```bash
git switch -c challenge-01-ana-perez
```

Utiliza las siguientes reglas para nombrar la rama:

- Escribe todo en minúsculas.
- No utilices espacios.
- No utilices tildes.
- No utilices la letra `ñ`.
- Separa las palabras con guiones.
- Incluye el número del reto.
- Incluye tu nombre y apellido.

Ejemplos válidos:

```text
challenge-01-ana-perez
challenge-01-carlos-gomez
challenge-01-laura-restrepo
```

Ejemplos que debes evitar:

```text
Reto 1 Ana
challenge 01 juan
reto_1_José
final
mi-rama
```

---

# 9. Confirmar la rama actual

Ejecuta:

```bash
git branch
```

La rama activa aparecerá con un asterisco:

```text
* challenge-01-ana-perez
  main
```

También puedes ejecutar:

```bash
git status
```

El resultado debe indicar algo similar a:

```text
On branch challenge-01-ana-perez
```

No continúes si aparece:

```text
On branch main
```

Si todavía estás en `main`, crea la rama antes de modificar archivos:

```bash
git switch -c challenge-01-nombre-apellido
```

---

# 10. Ubicar la plantilla del notebook

La plantilla del Reto 1 se encuentra en:

```text
challenges/challenge_01_bandits/submission/reto_01_apellido_nombre.ipynb
```

Antes de comenzar, debes cambiar el nombre del notebook.

Por ejemplo, si tu nombre es Ana Pérez, el archivo debe llamarse:

```text
reto_01_perez_ana.ipynb
```

Usa primero el apellido y después el nombre.

No utilices:

- Espacios.
- Tildes.
- Eñes.
- Mayúsculas.
- Caracteres especiales.
- Nombres genéricos como `final.ipynb`.

---

# 11. Cambiar el nombre del notebook en Visual Studio Code

Desde el explorador de archivos de Visual Studio Code:

