"""
ETL 01 - Carga, limpieza y agregación mensual Tarea-02

Lee archivos desde:
  data/raw/

Escribe datasets preparados en:
  data/prep/

Escribe outputs de control (opcionales) en:
  artifacts/

Uso:
  python src/etl.py
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

# --- Rutas del repo Tarea-02 ---
# REPO_ROOT = Path(__file__).resolve().parents[1]  # asumiendo script en /src
# RAW_DIR = REPO_ROOT / "data" / "raw"
# PREP_DIR = REPO_ROOT / "data" / "prep"


# ----------------------------
# Utilidades de rutas
# ----------------------------
def find_repo_root(start: Path) -> Path:
    """
    Encuentra el root de la Tarea-02 buscando la carpeta:
        tarea-02/data

    El script debe vivir dentro de tarea-02 (por ejemplo en tarea-02/src).
    """
    cur = start.resolve()

    for _ in range(10):
        if cur.name == "tarea-02" and (cur / "data").exists():
            return cur
        cur = cur.parent

    raise RuntimeError(
        "No se encontró la carpeta 'tarea-02/data'. "
        "Asegúrate de ejecutar el script desde dentro de la carpeta tarea-02."
    )
# ----------------------------
# Lectura de insumos
# ----------------------------
def load_raw_data(raw_dir: Path) -> dict[str, pd.DataFrame]:
    required = [
        "sales_train.csv",
        "test.csv",
        "items_en.csv",
        "shops_en.csv",
        "item_categories_en.csv",
        "sample_submission.csv",
    ]

    missing = [f for f in required if not (raw_dir / f).exists()]
    if missing:
        raise FileNotFoundError(
            f"Faltan archivos en {raw_dir}:\n- " + "\n- ".join(missing)
        )

    return {
        "sales": pd.read_csv(raw_dir / "sales_train.csv"),
        "test": pd.read_csv(raw_dir / "test.csv"),
        "items": pd.read_csv(raw_dir / "items_en.csv"),
        "shops": pd.read_csv(raw_dir / "shops_en.csv"),
        "cats": pd.read_csv(raw_dir / "item_categories_en.csv"),
        "sample": pd.read_csv(raw_dir / "sample_submission.csv"),
    }


# ----------------------------
# Transformaciones
# ----------------------------
def build_enriched_sales(df_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
    sales = df_dict["sales"]
    items = df_dict["items"]
    shops = df_dict["shops"]
    cats = df_dict["cats"]

    df = (
        sales.merge(items, on="item_id", how="left")
             .merge(shops, on="shop_id", how="left")
             .merge(cats, on="item_category_id", how="left")
    )

    # Tipos
    df["item_price"] = pd.to_numeric(df["item_price"], errors="coerce")
    df["item_cnt_day"] = pd.to_numeric(df["item_cnt_day"], errors="coerce")

    # Fecha
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="coerce")

    # KPI base: ventas diarias
    df["sales"] = (df["item_cnt_day"] * df["item_price"]).astype(float)

    # Años/mes para control rápido
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    return df


def build_yearly_control(df: pd.DataFrame) -> pd.DataFrame:
    yearly = (
        df.groupby("year", as_index=False)
          .agg(
              total_sales=("sales", "sum"),
              total_units=("item_cnt_day", "sum"),
              num_transactions=("item_cnt_day", "size"),
              avg_price=("item_price", "mean"),
              active_products=("item_id", "nunique"),
              active_shops=("shop_id", "nunique"),
          )
    )
    return yearly


def build_monthly_with_lags(df: pd.DataFrame) -> pd.DataFrame:
    # Agregación mensual (month-end)
    monthly = (
        df.groupby([pd.Grouper(key="date", freq="M"), "shop_id", "item_id", "item_name"], as_index=False)
          .agg(
              monthly_sales=("sales", "sum"),
              monthly_units=("item_cnt_day", "sum"),
              avg_price=("item_price", "mean"),
              min_price=("item_price", "min"),
              max_price=("item_price", "max"),
              num_transactions=("item_cnt_day", "size"),
              active_days=("date", lambda s: s.dt.date.nunique()),
          )
    )

    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month

    # Orden para lags
    monthly = monthly.sort_values(["shop_id", "item_id", "year", "month"]).reset_index(drop=True)

    # Lags (1 mes)
    monthly["monthly_sales_lag_1"] = monthly.groupby(["shop_id", "item_id"])["monthly_sales"].shift(1)
    monthly["monthly_units_lag_1"] = monthly.groupby(["shop_id", "item_id"])["monthly_units"].shift(1)

    # Fill solo lags
    monthly[["monthly_sales_lag_1", "monthly_units_lag_1"]] = (
        monthly[["monthly_sales_lag_1", "monthly_units_lag_1"]].fillna(0)
    )

    return monthly


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    repo_root = find_repo_root(Path(__file__))
    raw_dir = repo_root / "data" / "raw"
    prep_dir = repo_root / "data" / "prep"
    artifacts_dir = repo_root / "artifacts"

    prep_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # 1) Load
    df_dict = load_raw_data(raw_dir)

    # 2) Build enriched dataset
    df = build_enriched_sales(df_dict)
    print(f"[OK] df enriched shape: {df.shape}")

    # 3) Controles (ejecutivo / sanity checks)
    yearly_control = build_yearly_control(df)
    yearly_control_path = artifacts_dir / "yearly_control.csv"
    yearly_control.to_csv(yearly_control_path, index=False)
    print(f"[OK] Saved yearly control: {yearly_control_path}")

    # 4) Monthly + lags
    monthly = build_monthly_with_lags(df)
    print(f"[OK] monthly with lags shape: {monthly.shape}")

    # 5) Save outputs (Tarea-02 -> data/prep)
    df_out = prep_dir / "df_base.parquet"
    monthly_out = prep_dir / "monthly_with_lags.parquet"
    monthly_csv_out = prep_dir / "monthly_with_lags.csv"

    df.to_parquet(df_out, index=False)
    monthly.to_parquet(monthly_out, index=False)
    monthly.to_csv(monthly_csv_out, index=False)

    print(f"[OK] Saved: {df_out}")
    print(f"[OK] Saved: {monthly_out}")
    print(f"[OK] Saved: {monthly_csv_out}")


if __name__ == "__main__":
    main()