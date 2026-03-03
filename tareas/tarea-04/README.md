# Tarea 04 - MLOps en Práctica — Docker, Git Workflow y Testing
 
El objetivo de esta tarea es implementar un **pipeline reproducible de datos y modelado**, siguiendo buenas prácticas de ingeniería de datos y MLOps.

---
## 📂 Estructura del Proyecto


```
tarea-04/
│
├── artifacts
│   ├── figures
│   ├── logs
│   │   ├── etl.log
│   │   ├── evaluate_20260207_085857.log
│   │   ├── predict_20260207_085856.log
│   │   ├── train_20260207_085839.log
│   ├── models
│   │   ├── lgbm_weekly_v1_info.json
│   │   └── lgbm_weekly_v1.pkl
│   ├── predictions
│   │   └── valid_predictions.parquet
│   ├── reports
│   │   ├── eda_demand_distribution.png
│   │   ├── estacionalidad.png
│   │   ├── modelos_images.png
│   │   └── pareto.png
│   └── yearly_control.csv
├── data
│   ├── inference
│   ├── predictions
│   ├── prep
│   │   ├── df_base.csv
│   │   ├── df_base.parquet
│   │   ├── monthly_with_lags.csv
│   │   └── monthly_with_lags.parquet
│   └── raw
│       ├── item_categories_en.csv
│       ├── item_categories.csv
│       ├── items_en.csv
│       ├── items.csv
│       ├── sales_train.csv
│       ├── sample_submission.csv
│       ├── shops_en.csv
│       ├── shops.csv
│       └── test.csv
├── main.py
├── notebooks
│   ├── 00_etl.ipynb
│   ├── 01_eda.ipynb
│   ├── 02_feature_engineering.ipynb
│   ├── 03_modeling.ipynb
│   └── 04_evaluation.ipynb
├── pyproject.toml
├── README.md
├── Resumen_Ejecutivo.md
├── src
│   ├── __init__.py
│   ├── config.py
│   ├── inference
│   │   ├── predict.py
│   │   └── test
│   │       └── test_inference.py
│   ├── processing
│   │   ├── etl.py
│   │   ├── features.py
│   │   ├── logging_config.py
│   │   └── test
│   │       └── test_prep.py
│   └── training
│       ├── evaluate.py
│       ├── test
│       │   └── test_train.py
│       └── train.py
└── uv.lock
```

## Convenios del proyecto

Este proyecto sigue una serie de **convenios estándar** para asegurar orden, reproducibilidad y escalabilidad.

---

### 📂 Organización de carpetas

- **`notebooks/`**
  - Uso exclusivo para:
    - EDA
    - Análisis exploratorio
    - Pruebas y prototipos
  - No debe contener lógica productiva final.

- **`src/`**
  - Contiene únicamente **código productivo**.
  - Cada script debe ser:
    - Reproducible
    - Ejecutable
    - Independiente del entorno interactivo.
  - No se ejecutan notebooks en producción.

- **`data/`**
  - `raw/`: datos originales (solo lectura).
  - `prep/`: datos transformados y listos para modelado.
  - `inference/`: datos usados para predicción batch.
  - `predictions/`: resultados de inferencia.

- **`artifacts/`**
  - Modelos entrenados
  - Reportes
  - Gráficos
  - Métricas
  - Cualquier salida generada por el pipeline

---

## 🔄 Flujo del Pipeline

```
Raw Data (data/raw)
    ↓
ETL (src/processing/etl.py)
    ↓
Feature Engineering (src/processing/features.py)
    ↓
Training (src/training/train.py)
    ↓
Evaluation (src/training/evaluate.py)
    ↓
Inference (src/inference/predict.py)
    ↓
Predictions (artifacts/predictions)


## Modelo de datos (ventas_pred)

Este es el modelo de datos utilizado en el pipeline de **ventas_pred** (ETL + agregación mensual con lags):

![Modelo de Datos ventas_pred](../../reports/Modelo_de_Datos.png)

### 🧪 Manejo de datos

- Los datos **no se versionan** en Git.
- Solo se versiona la **estructura de carpetas**.
- El formato estándar para datos intermedios es **Parquet**.
- Los CSV solo se permiten en `raw/` si vienen de la fuente original.

---

### 📦 Dependencias y entorno

- El proyecto utiliza **`uv`** para manejo de dependencias.
El proyecto incluye:
  - `pyproject.toml`
  - `uv.lock`
  
Principales librerías:

- boto3 (>= 1.42.34)
- jupyterlab (>= 4.5.2)
- kaggle (>= 1.8.3)
- lightgbm (>= 4.6.0)
- matplotlib (>= 3.10.8)
- numpy (>= 2.4.1)
- pandas (>= 3.0.0)
- pyarrow (>= 23.0.0)
- scikit-learn (>= 1.8.0)
- black
- pylint
- ruff


### Instalación del ambiente

Desde la carpeta de la tarea/proyecto:

bash
uv sync

Este comando:
	•	Crea el entorno virtual si no existe
	•	Instala las dependencias definidas en pyproject.toml
	•	Garantiza reproducibilidad usando uv.lock

## Detalle de la ejecución del proyecto

Esta sección describe **cómo ejecutar el pipeline del proyecto** de forma correcta y reproducible, siguiendo los convenios definidos.

---

### 📍 Punto de partida

Todos los comandos deben ejecutarse **desde la raíz de la tarea**, por ejemplo:

bash
cd tareas/tarea-03
uv sync
uv run python src/etl.py
uv run python src/features.py
uv run python src/train.py
uv run python src/predict.py

Flujo recomendado: 

raw → etl → prep → features → train → model → predict → predictions

## ✅ Calidad del código y Linting

Para garantizar **calidad, consistencia y mantenibilidad** del código, este proyecto adopta herramientas de **linting y formateo automático**. Estas prácticas ayudan a detectar errores temprano, mantener un estilo uniforme y facilitar el trabajo colaborativo.

### 🎯 Objetivos

- Detectar errores antes de ejecutar el código
- Mantener un estilo consistente en todo el proyecto
- Seguir las mejores prácticas de Python (PEP 8)
- Reducir fricción en revisiones de código (code reviews)
- Facilitar la transición de notebooks experimentales a código de producción

---

### 🔍 Linters y Formatters

Es importante distinguir entre dos tipos de herramientas:

#### Linters (detectan problemas)
- Analizan el código para detectar errores, malas prácticas y problemas de estilo. 

#### Formatters (corrigen el formato)
- Reformatean el código para seguir un estilo consistente
-- **Modifican** el código automáticamente

### Resultado de la evaluación

La siguiente imagen muestra el resultado de la evaluación de calidad del código aplicada al módulo de producción:

![Evaluación de calidad del código](../../reports/code_quality.png)

## Autor

	•	José Antonio Esparza
	•	Gustavo Pardo

- Repositorio desarrollado como parte del curso Métodos de Gran Escala.
