# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------
import subprocess
import logging as log
from logging import Logger
from pathlib import Path
from typing import List

import click
import tqdm

LOG_PATH = Path(__file__).parent / "tiff_fix.log"

# -----------------------------------------------------------------------------
# TIFF Fix
# -----------------------------------------------------------------------------


def tiff_fix(files: List[Path]) -> None:
    logger = log_setup("tiff_fix", LOG_PATH)
    for tiff in tqdm.tqdm(files, desc="Fixing TIFF files", unit="files"):
        cmd = ["i_view64.exe", tiff, "/convert", tiff, "/silent"]
        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except subprocess.CalledProcessError:
            logger.error(f"{tiff} failed")


def load_files(from_file: Path) -> List[Path]:
    with from_file.open(encoding="utf-8") as f:
        files = [Path(line.strip()) for line in f.readlines()]
    return files


def log_setup(log_name: str, log_file: Path) -> Logger:
    # Init & log to file
    logger: Logger = log.getLogger(log_name)
    file_handler = log.FileHandler(log_file, "w", encoding="utf-8")

    # Format
    log_fmt = log.Formatter(
        fmt="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler.setFormatter(log_fmt)

    # Handler & level
    logger.addHandler(file_handler)
    logger.setLevel(log.INFO)

    return logger


@click.command()
@click.argument(
    "file_list",
    type=click.Path(exists=True, file_okay=True, resolve_path=True),
)
def cli(file_list: str) -> None:
    files = load_files(Path(file_list))
    tiff_fix(files)
    click.echo(f"Finished fixing TIFF files. See log {LOG_PATH} for details.")


if __name__ == "__main__":
    cli()
