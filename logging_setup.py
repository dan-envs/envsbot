"""
Logging configuration for BlueBot.

This module initializes the global logging system used by the bot and
its plugins. It provides colored console output for development and
rotating log files for persistent logging.

Usage
-----
from logging_setup import setup_logging
setup_logging()
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(debug: bool = False):
    """
    Initialize the logging system.

    Parameters
    ----------
    debug : bool
        Enable debug logging if True.
    """

    log_level = logging.DEBUG if debug else logging.INFO

    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "bluebot.log"

    # ------------------------------------------------------------------
    # Log format
    # ------------------------------------------------------------------

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    # ------------------------------------------------------------------
    # Console handler
    # ------------------------------------------------------------------

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(formatter)

    # ------------------------------------------------------------------
    # Rotating file handler
    # ------------------------------------------------------------------

    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=2_000_000,   # 2 MB
        backupCount=5
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # ------------------------------------------------------------------
    # Root logger
    # ------------------------------------------------------------------

    logging.basicConfig(
        level=log_level,
        handlers=[console, file_handler]
    )
