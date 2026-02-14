"""
Evaluación del modelo.

- Lee artifacts/predictions/valid_predictions.parquet
- Calcula MAE/RMSE
- Calcula baseline naive (t-1 por shop-item) sobre el mismo dataset
- Guarda artifacts/reports/metrics.json
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import ModelConfig, PathsConfig, find_repo_root
from src.logging_config import get_logger


def evaluate() -> None:
    """Evalua las predicciones"""

    repo_root = find_repo_root(Path(__file__))
    paths = PathsConfig.from_repo_root(repo_root)
    cfg = ModelConfig()

    logger = get_logger("evaluate", paths)
    start_time = time.time()

    paths.reports_dir.mkdir(parents=True, exist_ok=True)

    pred_path = paths.predictions_dir / "valid_predictions.parquet"
    if not pred_path.exists():
        raise FileNotFoundError(
            f"No existe {pred_path}. Corre primero: uv run python src/predict.py"
        )

    df_pred = pd.read_parquet(pred_path)
    y_true = df_pred[cfg.target_col]
    y_pred = df_pred["y_pred"]

    mae = float(mean_absolute_error(y_true, y_pred))
    rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))

    # Baseline naive: y_hat(t) = y(t-1) por shop-item
    key_1, key_2 = cfg.key_cols
    df_sorted = df_pred.sort_values([key_1, key_2, cfg.time_col]).copy()
    df_sorted["naive_pred"] = df_sorted.groupby([key_1, key_2])[cfg.target_col].shift(1)
    df_naive = df_sorted.dropna(subset=["naive_pred"]).copy()

    mae_naive = float(
        mean_absolute_error(df_naive[cfg.target_col], df_naive["naive_pred"])
    )
    rmse_naive = float(
        np.sqrt(mean_squared_error(df_naive[cfg.target_col], df_naive["naive_pred"]))
    )

    metrics = {
        "mae": mae,
        "rmse": rmse,
        "mae_naive": mae_naive,
        "rmse_naive": rmse_naive,
        "delta_mae": mae_naive - mae,
        "delta_rmse": rmse_naive - rmse,
        "n_eval_rows": int(len(df_pred)),
        "n_naive_rows": int(len(df_naive)),
    }

    out_path = paths.reports_dir / "metrics.json"
    out_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")

    duration = time.time() - start_time
    logger.info("MAE: %.6f | RMSE: %.6f", mae, rmse)
    logger.info("Naive MAE: %.6f | Naive RMSE: %.6f", mae_naive, rmse_naive)
    logger.info("ΔMAE: %.6f | ΔRMSE: %.6f", metrics["delta_mae"], metrics["delta_rmse"])
    logger.info("Metrics guardadas en: %s", out_path)
    logger.info("Evaluate finalizado en %.2f segundos", duration)


if __name__ == "__main__":
    evaluate()
