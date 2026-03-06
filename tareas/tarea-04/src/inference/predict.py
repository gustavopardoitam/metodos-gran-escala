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
from processing.features import build_features, make_modeling_dataset, temporal_split
from logging_config import get_logger
import argparse
from typing import Sequence



###Argparse
def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="inference",
        description="Generación de predicciones batch",
    )

    parser.add_argument(
        "--input-path",
        type=str,
        default=None,
        help="Ruta al dataset preparado. Si no se especifica, usa data/prep/<dataset_filename>",
    )

    parser.add_argument(
        "--model-path",
        type=str,
        default=None,
        help="Ruta al modelo entrenado. Si no se especifica, usa artifacts/models/model.pkl",
    )

    parser.add_argument(
        "--output-path",
        type=str,
        default=None,
        help="Ruta de salida para las predicciones. Si no se especifica, usa artifacts/predictions/valid_predictions.parquet",
    )

    parser.add_argument(
        "--clip-min",
        type=float,
        default=None,
        help="Valor mínimo para clipping de predicciones. Si no se especifica, usa cfg.clip_pred_min",
    )

    return parser.parse_args(argv)

def predict(
    input_path: Path | None = None,
    model_path: Path | None = None,
    output_path: Path | None = None,
    clip_min: float | None = None,
    ) -> None:
    repo_root = find_repo_root(Path(__file__))
    paths = PathsConfig.from_repo_root(repo_root)
    cfg = ModelConfig()

    logger = get_logger("predict", paths)
    start_time = time.time()

    paths.predictions_dir.mkdir(parents=True, exist_ok=True)

    resolved_model_path = model_path or (paths.models_dir / "model.pkl")
    if not resolved_model_path.exists():
        raise FileNotFoundError(
            f"No existe el modelo en {resolved_model_path}. "
            "Corre primero: uv run python -m training"
        )

    resolved_input_path = input_path or (paths.data_prep / cfg.dataset_filename)
    if not resolved_input_path.exists():
        raise FileNotFoundError(
            f"No existe el dataset preparado: {resolved_input_path}. "
            "Corre primero: uv run python -m processing"
        )

    resolved_output_path = output_path or (
        paths.predictions_dir / "valid_predictions.parquet"
    )
    resolved_output_path.parent.mkdir(parents=True, exist_ok=True)

    effective_clip_min = cfg.clip_pred_min if clip_min is None else clip_min

    logger.info("Cargando modelo y dataset...")
    model = joblib.load(resolved_model_path)
    df = pd.read_parquet(resolved_input_path)

    df_feat = build_features(df, cfg)
    df_model, feature_cols = make_modeling_dataset(df_feat, cfg)

    _, valid_df = temporal_split(df_model, cfg)

    x_valid = valid_df[feature_cols]
    pred = model.predict(x_valid)
    pred = np.clip(pred, effective_clip_min, None)

    out = valid_df[[*cfg.key_cols, cfg.time_col, cfg.target_col]].copy()
    out["y_pred"] = pred

    out.to_parquet(resolved_output_path, index=False)

    duration = time.time() - start_time
    logger.info("Predicciones guardadas: %s filas", f"{len(out):,}")
    logger.info("Archivo: %s", resolved_output_path)
    logger.info("Predict finalizado en %.2f segundos", duration)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)

    predict(
        input_path=Path(args.input_path) if args.input_path else None,
        model_path=Path(args.model_path) if args.model_path else None,
        output_path=Path(args.output_path) if args.output_path else None,
        clip_min=args.clip_min,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())