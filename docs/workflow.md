# Flujo de trabajo con Git y GitHub

Cada entrega debe realizarse mediante una rama y un Pull Request.

## Flujo general

```text
Actualizar main
      ↓
Crear una rama
      ↓
Resolver el reto
      ↓
Ejecutar pruebas
      ↓
Crear un commit
      ↓
Hacer push
      ↓
Crear un Pull Request
      ↓
Revisar GitHub Actions
      ↓
Atender comentarios
```

## 1. Abrir el repositorio

Abre Docker Desktop.

Después abre el repositorio:

```bash
cd rl-course_EIA_20262
code .
```

En Visual Studio Code selecciona:

```text
Dev Containers: Reopen in Container
```

## 2. Revisar el estado

```bash
git status
```

Este comando muestra:

- La rama actual.
- Los archivos modificados.
- Los archivos preparados para commit.
- Los archivos que todavía no están siendo rastreados.

## 3. Cambiar a main

```bash
git switch main
```

## 4. Descargar actualizaciones

```bash
git pull origin main
```

Debes hacer esto antes de comenzar cada reto.

## 5. Crear una rama

Utiliza esta convención:

```text
challenge-XX-nombre-apellido
```

Ejemplo:

```bash
git switch -c challenge-01-juan-perez
```

