"""
Predicción usando el modelo entrenado.

- Carga artifacts/models/model.pkl y model_info.json
- Reconstruye features igual que train
- Genera predicciones para el "valid" (split temporal)
- Guarda artifacts/predictions/valid_predictions.parquet
"""

from __future__ import annotations

import time
from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from src.config import ModelConfig, PathsConfig, find_repo_root
from src.features import build_features, make_modeling_dataset, temporal_split
from src.logging_config import get_logger


def predict() -> None:
    repo_root = find_repo_root(Path(__file__))
    paths = PathsConfig.from_repo_root(repo_root)
    cfg = ModelConfig()

    logger = get_logger("predict", paths)
    start_time = time.time()

    paths.predictions_dir.mkdir(parents=True, exist_ok=True)

    model_path = paths.models_dir / "model.pkl"
    if not model_path.exists():
        raise FileNotFoundError(
            f"No existe el modelo en {model_path}. Corre primero: uv run python src/train.py"
        )

    dataset_path = paths.data_prep / cfg.dataset_filename
    if not dataset_path.exists():
        raise FileNotFoundError(
            f"No existe el dataset preparado: {dataset_path}. Corre primero: uv run python src/etl.py"
        )

    logger.info("Cargando modelo y dataset...")
    model = joblib.load(model_path)
    df = pd.read_parquet(dataset_path)

    df_feat = build_features(df, cfg)
    df_model, feature_cols = make_modeling_dataset(df_feat, cfg)

    train_df, valid_df = temporal_split(df_model, cfg)

    x_valid = valid_df[feature_cols]
    pred = model.predict(x_valid)
    pred = np.clip(pred, cfg.clip_pred_min, None)

    out = valid_df[[*cfg.key_cols, cfg.time_col, cfg.target_col]].copy()
    out["y_pred"] = pred

    out_path = paths.predictions_dir / "valid_predictions.parquet"
    out.to_parquet(out_path, index=False)

    duration = time.time() - start_time
    logger.info("Predicciones guardadas: %s filas", f"{len(out):,}")
    logger.info("Archivo: %s", out_path)
    logger.info("Predict finalizado en %.2f segundos", duration)


if __name__ == "__main__":
    predict()
