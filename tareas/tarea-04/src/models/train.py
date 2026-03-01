"""
Entrenamiento del modelo.

Flujo:
- Lee data/prep/monthly_with_lags.parquet
- Genera features (lags/rolls)
- Split temporal
- Entrena LightGBM con fallback
- Guarda modelo + metadata en artifacts/models
"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import ModelConfig, PathsConfig, find_repo_root
from src.features import build_features, make_modeling_dataset, temporal_split
from src.logging_config import get_logger


def _load_dataset(paths: PathsConfig, cfg: ModelConfig) -> pd.DataFrame:
    dataset_path = paths.data_prep / cfg.dataset_filename
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"No existe el dataset preparado: {dataset_path}. "
            "Corre primero: uv run python src/etl.py"
        )
    return pd.read_parquet(dataset_path)


def _naive_baseline_rmse(df: pd.DataFrame, cfg: ModelConfig) -> tuple[float, float]:
    key_1, key_2 = cfg.key_cols
    target = cfg.target_col
    time_col = cfg.time_col

    df_sorted = df.sort_values([key_1, key_2, time_col]).copy()
    df_sorted["naive_pred"] = df_sorted.groupby([key_1, key_2])[target].shift(1)
    df_naive = df_sorted.dropna(subset=["naive_pred"]).copy()

    mae = mean_absolute_error(df_naive[target], df_naive["naive_pred"])
    rmse = float(np.sqrt(mean_squared_error(df_naive[target], df_naive["naive_pred"])))
    return float(mae), rmse


def _train_model(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_valid: pd.DataFrame,
    y_valid: pd.Series,
    cfg: ModelConfig,
) -> tuple[Any, np.ndarray]:
    try:
        import lightgbm as lgb  # pylint: disable=import-error

        model = lgb.LGBMRegressor(
            n_estimators=5000,
            learning_rate=0.03,
            num_leaves=63,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=cfg.random_state,
            n_jobs=-1,
        )
        model.fit(
            x_train,
            y_train,
            eval_set=[(x_valid, y_valid)],
            eval_metric="rmse",
            callbacks=[lgb.early_stopping(stopping_rounds=50, verbose=False)],
        )
        pred = model.predict(x_valid)
        return model, pred
    except Exception:
        model = GradientBoostingRegressor(random_state=cfg.random_state)
        model.fit(x_train, y_train)
        pred = model.predict(x_valid)
        return model, pred


def train() -> None:
    repo_root = find_repo_root(Path(__file__))
    paths = PathsConfig.from_repo_root(repo_root)
    cfg = ModelConfig()

    paths.models_dir.mkdir(parents=True, exist_ok=True)

    logger = get_logger("train", paths)
    start_time = time.time()

    logger.info("Iniciando entrenamiento...")

    df = _load_dataset(paths, cfg)
    logger.info("Dataset cargado: %s filas, %s columnas", f"{len(df):,}", df.shape[1])

    df_feat = build_features(df, cfg)
    df_model, feature_cols = make_modeling_dataset(df_feat, cfg)
    logger.info(
        "Dataset de modelado: %s filas, %s features",
        f"{len(df_model):,}",
        len(feature_cols),
    )

    mae_naive, rmse_naive = _naive_baseline_rmse(df_model, cfg)
    logger.info("Baseline naive -> MAE: %.6f | RMSE: %.6f", mae_naive, rmse_naive)

    train_df, valid_df = temporal_split(df_model, cfg)
    logger.info(
        "Split temporal -> train: %s | valid: %s", train_df.shape, valid_df.shape
    )

    x_train = train_df[feature_cols]
    y_train = train_df[cfg.target_col]
    x_valid = valid_df[feature_cols]
    y_valid = valid_df[cfg.target_col]

    model, pred = _train_model(x_train, y_train, x_valid, y_valid, cfg)

    pred = np.clip(pred, cfg.clip_pred_min, None)
    mae = float(mean_absolute_error(y_valid, pred))
    rmse = float(np.sqrt(mean_squared_error(y_valid, pred)))

    logger.info("Modelo -> MAE: %.6f | RMSE: %.6f", mae, rmse)
    logger.info(
        "Mejora vs naive -> ΔMAE: %.6f | ΔRMSE: %.6f",
        mae_naive - mae,
        rmse_naive - rmse,
    )

    model_path = paths.models_dir / "model.pkl"
    metadata_path = paths.models_dir / "model_info.json"

    joblib.dump(model, model_path)

    info = {
        "model_path": str(model_path.name),
        "dataset": cfg.dataset_filename,
        "target": cfg.target_col,
        "time_col": cfg.time_col,
        "features": feature_cols,
        "n_features": len(feature_cols),
        "clip_pred_min": cfg.clip_pred_min,
        "metrics": {
            "mae": mae,
            "rmse": rmse,
            "mae_naive": mae_naive,
            "rmse_naive": rmse_naive,
        },
    }
    metadata_path.write_text(json.dumps(info, indent=2), encoding="utf-8")

    duration = time.time() - start_time
    logger.info("Entrenamiento finalizado en %.2f segundos", duration)
    logger.info("Modelo guardado en: %s", model_path)
    logger.info("Metadata guardada en: %s", metadata_path)


if __name__ == "__main__":
    train()
