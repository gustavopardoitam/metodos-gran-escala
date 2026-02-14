"""
Entry-point del pipeline.

Permite correr:
- all (etl -> train -> predict -> evaluate)
- o steps individuales
"""

from __future__ import annotations

import argparse

from src.etl import main as etl_main
from src.train import train
from src.predict import predict
from src.evaluate import evaluate
from src.logging_config import configure_root_logging

configure_root_logging()

def run_all() -> None:
    etl_main()
    train()
    predict()
    evaluate()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pipeline production-ready: ETL -> Train -> Predict -> Evaluate")
    parser.add_argument(
        "--step",
        choices=("all", "etl", "train", "predict", "evaluate"),
        default="all",
        help="Paso a ejecutar",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.step == "all":
        run_all()
    elif args.step == "etl":
        etl_main()
    elif args.step == "train":
        train()
    elif args.step == "predict":
        predict()
    elif args.step == "evaluate":
        evaluate()


if __name__ == "__main__":
    main()
