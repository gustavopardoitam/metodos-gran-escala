# Instrucciones  - Tarea 01: Métodos Gran Escala

**Proyecto**: EDA y preparación de datos para pronóstico de ventas (dataset Kaggle retail sales)

**Flujo**: `etl_01_download.ipynb` (setup) → `data/processed/df_base.csv` → `EDA_01.ipynb` (análisis)

### Datos
- **Raw** (`data/raw/`): `sales_train.csv` (ventas históricas), `test.csv`, `items_en.csv`, `shops_en.csv`, `item_categories_en.csv`, `sample_submission.csv`
- **Procesados**: `df_base.csv` (tablas fusionadas por `item_id`, `shop_id`, `item_category_id`; columna `sales = item_cnt_day * item_price`; fechas en datetime)
### Patrones Pandas
- **Conversión de tipos**: `item_price` → `float`, `item_cnt_day` → numérico
- **Fechas**: `pd.to_datetime(df["date"], format="%d.%m.%Y")` (formato español)
- **Rutas**: `pathlib.Path` con constantes (`RAW = Path("data/raw")`, `PROCESSED = Path("data/processed")`)
- **Groupby→Agg**: `df.groupby([keys], as_index=False).agg({col: func})`
- **Top-N**: Extraer IDs con `.tolist()`, filtrar con `.isin()`
- **Series de tiempo**: Agregar `year` temprano; agregar por mes/año

### Setup
```bash
python -m venv .venv && source .venv/bin/activate
uv sync
```

Ejecutar: `etl_01_download.ipynb` (genera `df_base.csv`) → `EDA_01.ipynb` (análisis)

## Detalles Clave

- **Pareto (80/20)**: Identificar productos que generan 80% ingresos para segmentación ABC
- **Estacionalidad**: Top 5 productos → patrones anuales/mensuales, tendencias vs ciclos
- **Trampas**: 
  - Formato fecha es "dd.mm.yyyy" → especificar en `pd.to_datetime(..., format="%d.%m.%Y")`
  - Validar tras fusiones: comparar shape antes/después
  - Usar columnas en inglés (no mezclar con `items.csv`)
- **Visualización**: matplotlib en línea en Jupyter, outputs PNG
- **Validación**: Visual (gráficos + outputs de celdas); verificar shapes intermedias y muestras
