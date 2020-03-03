import pyautogui
import pyperclip


def copypaste(str_to_copy: str) -> None:
    pyperclip.copy(f"{str_to_copy}")
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")
