from pathlib import Path
from datetime import datetime
import threading
import subprocess
import sys

import pyperclip
import keyboard
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox


SAVE_PATH = Path("E:/memo/memo/clip")
HOTKEY = "ctrl+alt+a"

SAVE_PATH.mkdir(parents=True, exist_ok=True)

last_saved = ""


def create_icon_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill="white")
    draw.text((24, 22), "A", fill="black")
    return image


def show_confirm_window(content: str) -> bool:
    PREVIEW_LENGTH = 300
    preview = content[:PREVIEW_LENGTH]
    if len(content) > PREVIEW_LENGTH:
        preview += "\n\n...(생략)..."

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    result = messagebox.askyesno(
        "Clip Saver",
        f"이 내용을 저장할까?\n\n{preview}"
    )

    root.destroy()
    return result


def save_clipboard():
    global last_saved

    content = pyperclip.paste().strip()

    if not content:
        messagebox.showinfo("Clip Saver", "클립보드가 비어있어.")
        return

    if content == last_saved:
        messagebox.showinfo("Clip Saver", "이미 저장한 내용이야.")
        return

    if not show_confirm_window(content):
        return

    now = datetime.now()
    filename = now.strftime("%Y-%m-%d_%H%M%S.md")

    md = f"""---
created: {now.strftime("%Y-%m-%d %H:%M:%S")}
type: ai-log
---

{content}
"""

    path = SAVE_PATH / filename
    path.write_text(md, encoding="utf-8")

    last_saved = content

    messagebox.showinfo("Clip Saver", f"저장 완료\n\n{path}")


def open_save_folder(icon=None, item=None):
    subprocess.Popen(f'explorer "{SAVE_PATH}"')


def quit_app(icon, item):
    keyboard.unhook_all_hotkeys()
    icon.stop()
    sys.exit()


def register_hotkey():
    keyboard.add_hotkey(HOTKEY, save_clipboard)


def main():
    register_hotkey()

    icon = pystray.Icon(
        "Clip Saver",
        create_icon_image(),
        "Clip Saver",
        menu=pystray.Menu(
            pystray.MenuItem("저장 폴더 열기", open_save_folder),
            pystray.MenuItem("종료", quit_app)
        )
    )

    icon.run()


if __name__ == "__main__":
    main()