# Solución de problemas

## Docker Desktop no está abierto

### Síntoma

Aparece un error similar a:

```text
Cannot connect to the Docker daemon
```

### Solución

1. Abre Docker Desktop.
2. Espera hasta que Docker esté listo.
3. Ejecuta:

```bash
docker info
```

## El comando docker no existe

### Solución

1. Confirma que Docker Desktop esté instalado.
2. Reinicia el computador.
3. Abre una terminal nueva.
4. Ejecuta:

```bash
docker --version
```

## No aparece Reopen in Container

### Solución

1. Abre las extensiones de Visual Studio Code.
2. Busca `Dev Containers`.
3. Instala la extensión de Microsoft.
4. Reinicia Visual Studio Code.

## Error al construir el contenedor

Ejecuta:

```bash
docker compose build --no-cache
```

Si continúa:

```bash
docker compose logs
```

Copia el mensaje completo del error cuando solicites ayuda.

## Se modificó requirements.txt

Reconstruye el contenedor:

1. Presiona `Ctrl + Shift + P`.
2. Selecciona:

```text
Dev Containers: Rebuild Container
```

## Pytest no encuentra los módulos

Confirma que ejecutas `pytest` desde:

```text
/workspace
```

Verifica:

```bash
pwd
```

Después ejecuta:

```bash
pytest
```

## Git no reconoce el repositorio

Verifica:

```bash
git status
```

Si aparece un error de directorio seguro, ejecuta:

```bash
git config --global --add safe.directory /workspace
```

## Git no permite hacer push

Posibles causas:

- No tienes acceso de escritura.
- No has iniciado sesión en GitHub.
- La rama remota no está configurada.
- Estás intentando modificar una rama protegida.

Para publicar una rama por primera vez:

```bash
git push -u origin NOMBRE_DE_LA_RAMA
```

## No puedo hacer push a main

Esto puede ser intencional. Las entregas no deben enviarse directamente a `main`.

Crea una rama:

```bash
git switch -c challenge-01-nombre-apellido
```

Después publica esa rama:

```bash
git push -u origin challenge-01-nombre-apellido
```

## Hay cambios que no quiero conservar

Revisa primero:

```bash
git status
git diff
```

Para descartar los cambios de un archivo específico:

```bash
git restore RUTA_DEL_ARCHIVO
```

Este comando elimina cambios no guardados. Úsalo con cuidado.

## El Pull Request tiene conflictos

No elimines archivos ni fuerces el push.

Solicita ayuda al profesor o monitor e incluye:

- Nombre de la rama.
- Enlace al Pull Request.
- Captura del conflicto.
- Resultado de `git status`.

## Solicitar ayuda

Abre un Issue en:

https://github.com/Tejada90/rl-course_EIA_20262/issues

Incluye:

1. Sistema operativo.
2. Versión de Docker.
3. Versión de Git.
4. Comando ejecutado.
5. Mensaje completo del error.
6. Captura de pantalla, si es posible.

Comandos para obtener información:

```bash
docker --version
docker compose version
git --version
python --version
```
