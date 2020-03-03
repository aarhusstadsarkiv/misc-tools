import time
import pyautogui
import pyperclip
from pathlib import Path
import subprocess

pyautogui.PAUSE = 0.4
pyautogui.FAILSAFE = False


def copypaste(str_to_copy: str) -> None:
    pyperclip.copy(f"{str_to_copy}")
    pyautogui.hotkey("ctrl", "v", interval=0.1)


def save_as(file: str) -> None:
    pyautogui.press("f12")
    copypaste(file)
    pyautogui.press("tab")
    pyautogui.press("w")
    pyautogui.press("enter")
    time.sleep(0.5)
    pyautogui.press("enter")


def convert_doc_file(file: Path) -> None:
    out_file: Path = file.with_suffix(".docx")
    if out_file.is_file():
        out_file.unlink()
    subprocess.run(f"start {file}", shell=True)
    time.sleep(3)
    pyautogui.press("enter")
    time.sleep(0.5)
    save_as(out_file.name)
    time.sleep(1)
    pyautogui.hotkey("alt", "f4", interval=0.1)
    time.sleep(1)


convert_doc_file(Path("D:\\data\\test_data\\sammenskriv.Doc"))
