"""
Logging centralizado del proyecto.

Evita duplicar configuración de logging en cada script.
Crea logs en artifacts/logs y también imprime en consola.

Incluye prácticas básicas para evitar loggear info sensible.
"""

from __future__ import annotations

import logging
import socket
from datetime import datetime, timezone
from pathlib import Path

from src.config import PathsConfig


class UTCFormatter(logging.Formatter):
    """
    Formatter que fuerza timestamps en UTC y en formato ISO 8601 (con sufijo Z).
    """

    def formatTime(self, record, datefmt=None):  # noqa: N802 (firma esperada por logging)
        dt = datetime.fromtimestamp(record.created, tz=timezone.utc)
        return dt.isoformat(timespec="seconds").replace("+00:00", "Z")


class HostnameFilter(logging.Filter):
    """
    Asegura que el LogRecord tenga el atributo `hostname`,
    para soportar formatos que lo incluyan sin romper.
    """

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "hostname"):
            record.hostname = socket.gethostname()
        return True


def _ensure_dirs(paths: PathsConfig) -> None:
    paths.logs_dir.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, paths: PathsConfig) -> logging.Logger:
    """
    Crea/retorna un logger con handlers a archivo y consola.

    Parameters
    ----------
    name : str
        Nombre lógico (ej. "train", "predict").
    paths : PathsConfig
        Configuración de rutas del proyecto.

    Returns
    -------
    logging.Logger
        Logger configurado.
    """
    _ensure_dirs(paths)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Importante: evita duplicar logs si el root logger también tiene handlers
    logger.propagate = False

    # Evita duplicar handlers si se llama varias veces
    if logger.handlers:
        return logger

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    log_path = paths.logs_dir / f"{name}_{timestamp}.log"

    # Si quieres hostname, este formatter lo soporta (sin romper si no existiera)
    formatter = UTCFormatter(
        fmt="%(asctime)s - %(hostname)s - %(name)s - %(levelname)s - %(message)s"
    )

    hostname_filter = HostnameFilter()

    file_handler = logging.FileHandler(log_path, encoding="utf-8", mode="a")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(hostname_filter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(hostname_filter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    logger.info("Logger inicializado. Logfile=%s", log_path)

    return logger