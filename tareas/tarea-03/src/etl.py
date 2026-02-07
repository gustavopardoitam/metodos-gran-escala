"""
ETL 01 - Carga, limpieza y agregación mensual Tarea-03

Lee archivos desde:
  data/raw/

Escribe datasets preparados en:
  data/prep/

Escribe outputs de control (opcionales) en:
  artifacts/

Uso:
  uv run python src/etl.py
"""

from __future__ import annotations

from pathlib import Path
import logging
import socket
from datetime import datetime, timezone

import pandas as pd


# ----------------------------
# Logging
# ----------------------------
class UTCFormatter(logging.Formatter):
    """
    Formatter que fuerza timestamps en UTC y en formato ISO 8601 (con sufijo Z).
    """

    def formatTime(self, record, datefmt=None):  # noqa: N802 (firma esperada por logging)
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


def setup_logging(log_dir: Path) -> logging.LoggerAdapter:
    """
    Configura el sistema de logging del ETL.

    Los logs se escriben:
    - En consola
    - En artifacts/logs/etl.log

    Parameters
    ----------
    log_dir : pathlib.Path
        Directorio donde se almacenarán los logs.

    Returns
    -------
    logging.LoggerAdapter
        Logger con contexto (hostname) incluido en cada evento.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "etl.log"

    # Configurar logger con información contextual
    # (manteniendo tu idea: hostname dentro del formato)
    formatter = UTCFormatter(
        fmt="%(asctime)s - %(hostname)s - %(name)s - %(levelname)s - %(message)s"
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Evitar logs duplicados si se re-ejecuta en el mismo proceso (p. ej. notebook)
    root_logger.handlers.clear()

    # Handler a archivo
    file_handler = logging.FileHandler(log_file)  # append por default (mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # Handler a consola
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    root_logger.addHandler(file_handler)
    root_logger.addHandler(stream_handler)

    # Agregar hostname al log
    base_logger = logging.getLogger(__name__)
    logger_adapter = logging.LoggerAdapter(
        base_logger, {"hostname": socket.gethostname()}
    )

    return logger_adapter


# logger global (se inicializa en main)
logger: logging.LoggerAdapter


# ----------------------------
# Utilidades de rutas
# ----------------------------
def find_repo_root(start: Path) -> Path:
    """
    Encuentra el directorio raíz del proyecto de la tarea.

    El root se identifica buscando un archivo `pyproject.toml` y la carpeta `data/`
    en alguno de los directorios padre.
    """
    cur = start.resolve()
    for _ in range(10):
        if (cur / "pyproject.toml").exists() and (cur / "data").exists():
            return cur
        cur = cur.parent

    raise RuntimeError(
        "No se encontró el root del proyecto (pyproject.toml + data/). "
        "Ejecuta el script dentro de una carpeta de tarea (tareas/tarea-XX)."
    )


# ----------------------------
# Lectura de insumos
# ----------------------------
def load_raw_data(raw_dir: Path) -> dict[str, pd.DataFrame]:
    """
    Carga los archivos crudos requeridos desde `data/raw`.
    """
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

    logger.info("Cargando datos crudos desde %s", raw_dir)

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
    """
    Construye el dataset de ventas enriquecido tipo tabla de hechos.
    """
    logger.info("Construyendo dataset enriquecido tipo tabla de hechos")

    sales = df_dict["sales"]
    items = df_dict["items"]
    shops = df_dict["shops"]
    cats = df_dict["cats"]

    df = (
        sales.merge(items, on="item_id", how="left")
        .merge(shops, on="shop_id", how="left")
        .merge(cats, on="item_category_id", how="left")
    )

    df["item_price"] = pd.to_numeric(df["item_price"], errors="coerce")
    df["item_cnt_day"] = pd.to_numeric(df["item_cnt_day"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], format="%d.%m.%Y", errors="coerce")

    df["sales"] = (df["item_cnt_day"] * df["item_price"]).astype(float)
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    logger.info("Dataset enriquecido generado con shape %s", df.shape)
    return df


def build_yearly_control(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera métricas anuales de control.
    """
    logger.info("Generando métricas anuales cifras control")

    return df.groupby("year", as_index=False).agg(
        total_sales=("sales", "sum"),
        total_units=("item_cnt_day", "sum"),
        num_transactions=("item_cnt_day", "size"),
        avg_price=("item_price", "mean"),
        active_products=("item_id", "nunique"),
        active_shops=("shop_id", "nunique"),
    )


def build_monthly_with_lags(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla agregada mensual con variables lag.
    """
    logger.info("Construyendo agregado mensual con lags")

    monthly = df.groupby(
        [pd.Grouper(key="date", freq="ME"), "shop_id", "item_id", "item_name"],
        as_index=False,
    ).agg(
        monthly_sales=("sales", "sum"),
        monthly_units=("item_cnt_day", "sum"),
        avg_price=("item_price", "mean"),
        min_price=("item_price", "min"),
        max_price=("item_price", "max"),
        num_transactions=("item_cnt_day", "size"),
        active_days=("date", lambda s: s.dt.date.nunique()),
    )

    monthly["year"] = monthly["date"].dt.year
    monthly["month"] = monthly["date"].dt.month

    monthly = monthly.sort_values(["shop_id", "item_id", "year", "month"]).reset_index(
        drop=True
    )

    monthly["monthly_sales_lag_1"] = monthly.groupby(["shop_id", "item_id"])[
        "monthly_sales"
    ].shift(1)
    monthly["monthly_units_lag_1"] = monthly.groupby(["shop_id", "item_id"])[
        "monthly_units"
    ].shift(1)

    monthly[["monthly_sales_lag_1", "monthly_units_lag_1"]] = monthly[
        ["monthly_sales_lag_1", "monthly_units_lag_1"]
    ].fillna(0)

    logger.info("Agregado mensual generado con shape %s", monthly.shape)
    return monthly


# ----------------------------
# Main
# ----------------------------
def main() -> None:
    """
    Ejecuta el pipeline ETL completo para la Tarea-03.
    """
    global logger

    repo_root = find_repo_root(Path(__file__))
    logger = setup_logging(repo_root / "artifacts" / "logs")

    logger.info("🚀 Iniciando ETL Tarea-03")

    raw_dir = repo_root / "data" / "raw"
    prep_dir = repo_root / "data" / "prep"
    artifacts_dir = repo_root / "artifacts"

    prep_dir.mkdir(parents=True, exist_ok=True)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # 1) Load
    df_dict = load_raw_data(raw_dir)

    # 2) Build enriched dataset
    df = build_enriched_sales(df_dict)

    # 3) Controles
    yearly_control = build_yearly_control(df)
    yearly_control_path = artifacts_dir / "yearly_control.csv"
    yearly_control.to_csv(yearly_control_path, index=False)
    logger.info("Cifras Control anual guardado en %s", yearly_control_path)

    # 4) Monthly + lags
    monthly = build_monthly_with_lags(df)

    # 5) Outputs
    df_out_parquet = prep_dir / "df_base.parquet"
    monthly_out_parquet = prep_dir / "monthly_with_lags.parquet"
    df_out_csv = prep_dir / "df_base.csv"
    monthly_out_csv = prep_dir / "monthly_with_lags.csv"

    # 6) Save with parquet fallback
    try:
        df.to_parquet(df_out_parquet, index=False)
        monthly.to_parquet(monthly_out_parquet, index=False)
        logger.info(
            "Parquet guardado correctamente: %s y %s",
            df_out_parquet,
            monthly_out_parquet,
        )
    except Exception as e:
        logger.warning("Parquet no disponible (%s). Guardando CSV.", e)
        df.to_csv(df_out_csv, index=False)
        monthly.to_csv(monthly_out_csv, index=False)
        logger.info("CSV guardado en %s y %s", df_out_csv, monthly_out_csv)
    else:
        # Aunque parquet funcione, también guardamos CSV para inspección rápida
        df.to_csv(df_out_csv, index=False)
        monthly.to_csv(monthly_out_csv, index=False)
        logger.info("CSV guardado en %s y %s", df_out_csv, monthly_out_csv)

    logger.info("✅ ETL finalizado correctamente")


if __name__ == "__main__":
    main()
