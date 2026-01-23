# Métodos de Gran Escala

Repositorio de entregas y desarrollos para la materia **Métodos de Gran Escala**.

## Estructura del repositorio

- `tareas/`  
  Entregas individuales o en equipo por número de tarea.

- `proyectos/`  
  Proyectos integradores o finales.

## Reproducibilidad

Cada tarea/proyecto:
- usa `uv` para manejo de dependencias
- incluye `pyproject.toml` y `uv.lock`
- puede ejecutarse con:

```bash
uv sync
uv run <comando>

exit
exit()

