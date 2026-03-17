from __future__ import annotations

import argparse
import sys

from training.train import main as train_main
from training.evaluate import main as evaluate_main


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="training",
        description="Step de training: entrenamiento y evaluación"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("train", help="Entrenar modelo")
    subparsers.add_parser("evaluate", help="Evaluar predicciones del modelo")

    return parser.parse_known_args(argv)


def main(argv=None) -> int:
    args, remaining = parse_args(argv)

    if args.command == "train":
        return train_main(remaining)

    if args.command == "evaluate":
        return evaluate_main(remaining)

    raise ValueError(f"Comando no soportado: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))