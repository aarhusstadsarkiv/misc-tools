# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------

import multiprocessing
import logging
from pathlib import Path

# -----------------------------------------------------------------------------
# Logger
# -----------------------------------------------------------------------------


def log_setup(log_file: Path, mode: str = "w") -> logging.Logger:
    logger = logging.getLogger("Images2PDF")
    file_handler = logging.FileHandler(log_file, mode)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
    )
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger
