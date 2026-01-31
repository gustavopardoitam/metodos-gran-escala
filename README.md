# Métodos de Gran Escala

Repositorio de entregas y desarrollos para la materia **Métodos de Gran Escala**.

---

## Estructura del repositorio

```text
metodos-gran-escala/
├── tareas/        # Entregas por número de tarea
├── proyectos/     # Proyectos integradores o finales
├── README.md      # Este archivo
└── .gitignore
```
- `Carpeta tareas/`
  
Contiene las entregas individuales o en equipo organizadas por número de tarea.

```
tareas/
├── tarea-01/
├── tarea-02/
└── tarea-03/
```
Contiene las entregas individuales o en equipo organizadas por número de tarea.

Cada carpeta de tarea es autosuficiente y reproducible, y sigue una estructura estándar.

- `Carpeta proyectos/`
  
Contiene proyectos integradores o finales.La estructura es idéntica a la de una tarea, pero con mayor alcance y profundidad.

```
proyectos/
└── proyecto-final/
    ├── notebooks/
    ├── data/
    ├── src/
    ├── artifacts/
    ├── pyproject.toml
    └── README.md
```

## Reproducibilidad

Cada tarea o proyecto es reproducible de forma independiente.

- Usa `uv` para manejo de dependencias
- Incluye `pyproject.toml` y `uv.lock`

### Requisitos
- Python 3.10+
- uv

### Pasos para ejecutar

Desde la carpeta de la tarea o proyecto:

Cada tarea o proyecto:

- Usa `uv` para manejo de dependencias
- Incluye `pyproject.toml` y `uv.lock`

Puede ejecutarse con:

bash
uv sync
uv run <comando>

- O cualquier otro script definido en src/:

uv sync
uv run python src/etl.py


## Buenas prácticas adoptadas

	•	Separación clara entre exploración y producción
	•	Pipelines reproducibles
	•	Control de versiones con Git y ramas por tarea
	•	Ignorar datos pesados, versionar solo estructura
	•	Uso de parquet como formato estándar

## Autor

	•	José Antonio Esparza
	•	Gustavo Pardo

- Repositorio desarrollado como parte del curso Métodos de Gran Escala.