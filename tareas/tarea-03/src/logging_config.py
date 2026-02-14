"""
Logging centralizado del proyecto.

Evita duplicar configuración de logging en cada script.
Crea logs en artifacts/logs y también imprime en consola.

Incluye prácticas básicas para evitar loggear info sensible.
"""

from __future__ import annotations

import logging
from datetime import datetime
from src.config import PathsConfig
import socket
from pathlib import Path

class HostnameFilter(logging.Filter):
    """Inyecta hostname en cada LogRecord para que el formatter no falle."""

    def __init__(self) -> None:
        super().__init__()
        self._hostname = socket.gethostname()

    def filter(self, record: logging.LogRecord) -> bool:
        if not hasattr(record, "hostname"):
            record.hostname = self._hostname  # type: ignore[attr-defined]
        return True

def _ensure_dirs(paths: PathsConfig) -> None:
    paths.logs_dir.mkdir(parents=True, exist_ok=True)


def get_logger(name: str, paths: PathsConfig) -> logging.Logger:
    """
    Crea/retorna un logger con handlers a archivo y consola.

    Args:
        name: Nombre lógico (ej. "train", "predict").
        paths: Configuración de rutas del proyecto.

    Returns:
        Logger configurado.
    """
    _ensure_dirs(paths)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.propagate = False
    # Evita duplicar handlers si se llama varias veces
    if logger.handlers:
        return logger
    

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = paths.logs_dir / f"{name}_{timestamp}.log"

    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    hostname_filter = HostnameFilter()

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(hostname_filter)   
    
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    stream_handler.addFilter(hostname_filter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger


def configure_root_logging() -> None:
    """Configura el root logger para evitar formatos/handlers conflictivos."""
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.WARNING)  # root solo warnings+ para no ensuciar
