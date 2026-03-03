"""
Entry-point del pipeline.

Permite correr:
- all (etl -> train -> predict -> evaluate)
- o steps individuales
"""

from __future__ import annotations

import argparse


def run_all() -> None:
    from src.processing.etl import main as etl_main
    from src.training.train import train
    from src.inference.predict import predict
    from src.training.evaluate import evaluate

    etl_main()
    train()
    predict()
    evaluate()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Pipeline production-ready: ETL -> Train -> Predict -> Evaluate"
    )
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
        from src.processing.etl import main as etl_main

        etl_main()

    elif args.step == "train":
        from src.training.train import train

        train()

    elif args.step == "predict":
        from src.inference.predict import predict

        predict()

    elif args.step == "evaluate":
        from src.training.evaluate import evaluate

        evaluate()


if __name__ == "__main__":
    main()