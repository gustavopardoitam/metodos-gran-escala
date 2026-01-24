# Copilot Instructions - Tarea 01: Large Scale Methods

## Project Overview
This is an ML course assignment (Semestre 2, Métodos Gran Escala) that performs **EDA and data preparation for a sales forecasting dataset** using a Kaggle retail sales competition dataset. The workflow has two distinct phases:

1. **ETL Phase** (`etl_01_download.ipynb`): Data loading, merging, type casting, and feature engineering
2. **EDA Phase** (`EDA_01.ipynb`): Exploratory data analysis with time-series insights

## Architecture & Data Flow

### Data Structure
- **Raw data** (`data/raw/`): Six CSV files from Kaggle competition:
  - `sales_train.csv`: Historical daily sales records (date, shop_id, item_id, price, quantity)
  - `test.csv`: Test set for predictions
  - `items_en.csv`, `shops_en.csv`, `item_categories_en.csv`: Reference tables
  - `sample_submission.csv`: Required format template

- **Processed data** (`data/processed/df_base.csv`): Base dataframe created by ETL notebook
  - All tables merged on keys: `item_id`, `shop_id`, `item_category_id`
  - Computed column: `sales = item_cnt_day * item_price`
  - Date field cast to datetime (format: "dd.mm.yyyy" → pandas datetime)

### Typical Workflow
```
etl_01_download.ipynb (setup) → data/processed/df_base.csv → EDA_01.ipynb (analysis)
```

## Code Patterns & Conventions

### Pandas Operations
- **Type casting is critical**: Always convert `item_price` to `float`, `item_cnt_day` to numeric
- **Date handling**: Use `pd.to_datetime(df["date"], format="%d.%m.%Y")` (Spanish date format)
- **Path management**: Use `pathlib.Path` with constants like `RAW = Path("data/raw")`, `PROCESSED = Path("data/processed")`

### Analysis Patterns
- **Groupby → Aggregation flow**: Standard pattern is `df.groupby([key_cols], as_index=False).agg({col: func})`
- **Top-N filtering**: Extract IDs with `.tolist()` for downstream filtering with `.isin()`
- **Time-series processing**: Add `year` column early; compute monthly/yearly aggregations by grouping on `date` or `year`

### Notebook Structure
- **Minimal imports**: Only `pathlib.Path`, `pandas`, `numpy`, `matplotlib` (as of dependencies)
- **Inline calculations**: No separate modules; all analysis done within notebooks
- **Visualization**: Uses matplotlib for plots (e.g., Pareto analysis, seasonality charts)

## Development Setup

### Prerequisites
- Python ≥ 3.12
- UV package manager (modern alternative to pip/poetry)

### Initial Setup
```bash
# Create/activate virtual environment
python -m venv .venv
source .venv/bin/activate  # macOS/Linux

# Install dependencies (uses pyproject.toml)
uv sync
# or: pip install -e ".[dev]"
```

### Running Notebooks
1. **ETL (one-time setup)**: Execute `etl_01_download.ipynb` to generate `df_base.csv`
2. **EDA**: Execute `EDA_01.ipynb` cells sequentially (depends on `df_base.csv`)
   - **Note**: EDA is marked as "executed" with 193 cell execution events; ETL notebook shows as "not executed"

## Key Implementation Details

### Feature Definitions
- **Pareto principle (80/20)**: Identify products generating 80% of revenue; used for ABC segmentation
- **Seasonality**: Top 5 products analyzed for yearly/monthly patterns; detect trends vs. cyclical behavior
- **Time-based aggregations**: Group by year/month to observe trends; use `pandas.tseries.offsets.DateOffset` for rolling periods

### Common Pitfalls
- **Date format mismatch**: Raw dates are "dd.mm.yyyy" string; must specify in `pd.to_datetime(..., format="%d.%m.%Y")`
- **Missing validation**: After merges, verify no rows were dropped unexpectedly; compare shape before/after
- **Column naming**: Use English column names (cf. `items_en.csv` vs. `items.csv`); mixed-language naming creates confusion

## External Dependencies
- **Kaggle dataset**: Download via `kaggle` CLI (installed in `pyproject.toml`)
- **No external APIs**: Only local file I/O and pandas operations
- **Visualization outputs**: Charts rendered inline in Jupyter (PNG mime type in outputs)

## Testing & Validation
- **No test suite**: Verification is visual (notebook cell outputs, charts)
- **Validation approach**: Check intermediate dataframe shapes and sample rows at each stage
- **Output formats**: CSV export uses `df.to_csv(..., index=False)` for reproducibility
