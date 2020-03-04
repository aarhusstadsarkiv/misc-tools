import time
import json
import pyautogui
import logging
from typing import Any, List
from pathlib import Path
import subprocess
from tqdm import tqdm

pyautogui.PAUSE = 0.4
pyautogui.FAILSAFE = False


def log_setup(
    log_name: str, log_path: Path, mode: str = "w"
) -> logging.Logger:
    logger = logging.getLogger(log_name)
    log_file = f"{log_name}.log"
    if not log_path.is_dir():
        log_path.mkdir()
    file_handler = logging.FileHandler(log_path / log_file, mode)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s", datefmt="%H:%M:%S"
        )
    )
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def json_load(file: Path) -> Any:
    print(f"Loading {file}...", flush=True)
    return json.load(file.open(encoding="utf-8"))


def save_as(file: str) -> None:
    pyautogui.press("f12")
    time.sleep(1)
    pyautogui.press("tab")
    time.sleep(1)
    pyautogui.press("w")
    time.sleep(1)
    pyautogui.press("enter")
    time.sleep(1)
    pyautogui.press("enter")


def convert_doc_file(file: Path, log: logging.Logger) -> None:
    out_file: Path = file.with_suffix(".docx")
    if out_file.is_file():
        out_file.unlink()
    subprocess.run(["start", "winword", file], shell=True)
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(1)
    save_as(out_file.name)
    time.sleep(1)
    subprocess.run(["taskkill", "/f", "/im", "winword*"], capture_output=True)
    print(out_file, out_file.is_file())
    if not out_file.is_file():
        log.error(f"Failed to convert {file}")


def get_doc_files(data_file: Path) -> List[Path]:
    data = json_load(data_file)
    files = data.get("files", [])
    borked_files = []
    for file in files:

        file_puid = file.get("identification", {}).get("puid")
        file_ext = file.get("ext")
        if file_ext == ".doc" and file_puid == "fmt/101":
            borked_files.append(Path(file.get("path")))
    return borked_files


def main() -> None:
    log = log_setup(
        log_name="fix_doc_files",
        log_path=Path("D:\\data\\batches\\batch_1\\org_files\\_digiarch")
        / "logs",
        mode="w",
    )
    borked_files = get_doc_files(
        Path(
            "D:\\data\\batches\\batch_1\\org_files"
            "\\_digiarch\\.data\\data.json"
        )
    )
    for file in tqdm(borked_files, desc="Fixing files"):
        convert_doc_file(file, log)


if __name__ == "__main__":
    main()
