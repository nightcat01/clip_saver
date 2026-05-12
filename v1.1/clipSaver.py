from pathlib import Path
from datetime import datetime
import json
import re
import subprocess
import sys

import pyperclip
import keyboard
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox


APP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = APP_DIR / "config.json"
TEMPLATE_PATH = APP_DIR / "note_template.md"

DEFAULT_CONFIG = {
    "save_path": "E:/memo/memo/clip",
    "hotkey": "ctrl+alt+a",
    "preview_length": 300,
    "filename_format": "%Y-%m-%d_%H%M%S.md",
    "default_type": "ai-log",
    "default_tags": ["ai-log"],
    "default_title": "Clipboard Note",
    "source": "clipboard"
}

DEFAULT_TEMPLATE = """---
created: {{created}}
type: {{type}}
source: {{source}}
tags:
{{tags}}
---

# {{title}}

## Summary
{{summary}}

## Content
{{content}}
"""

last_saved = ""


def ensure_file(path: Path, content: str):
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def load_config() -> dict:
    ensure_file(
        CONFIG_PATH,
        json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2)
    )

    try:
        user_config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        messagebox.showerror(
            "Clip Saver",
            f"config.json 형식이 잘못됐어.\n\n{e}"
        )
        return DEFAULT_CONFIG.copy()

    return {**DEFAULT_CONFIG, **user_config}


def load_template() -> str:
    ensure_file(TEMPLATE_PATH, DEFAULT_TEMPLATE)
    return TEMPLATE_PATH.read_text(encoding="utf-8")


CONFIG = load_config()
SAVE_PATH = Path(CONFIG["save_path"])
HOTKEY = CONFIG["hotkey"]
PREVIEW_LENGTH = int(CONFIG["preview_length"])

SAVE_PATH.mkdir(parents=True, exist_ok=True)


def create_icon_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill="white")
    draw.text((24, 22), "A", fill="black")
    return image


def show_confirm_window(content: str) -> bool:
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


def sanitize_title(text: str) -> str:
    first_line = next((line.strip() for line in text.splitlines() if line.strip()), "")
    first_line = re.sub(r"^#+\s*", "", first_line)
    first_line = first_line[:80].strip()
    return first_line or CONFIG["default_title"]


def format_tags(tags) -> str:
    if not tags:
        return "  - untagged"
    return "\n".join(f"  - {tag}" for tag in tags)


def render_note(content: str, now: datetime) -> str:
    template = load_template()

    values = {
        "created": now.strftime("%Y-%m-%d %H:%M:%S"),
        "type": CONFIG["default_type"],
        "source": CONFIG["source"],
        "tags": format_tags(CONFIG.get("default_tags", [])),
        "title": sanitize_title(content),
        "summary": "",
        "content": content,
    }

    note = template
    for key, value in values.items():
        note = note.replace("{{" + key + "}}", str(value))

    return note


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
    filename = now.strftime(CONFIG["filename_format"])
    path = SAVE_PATH / filename

    path.write_text(render_note(content, now), encoding="utf-8")

    last_saved = content

    messagebox.showinfo("Clip Saver", f"저장 완료\n\n{path}")


def open_save_folder(icon=None, item=None):
    subprocess.Popen(f'explorer "{SAVE_PATH}"')


def open_config_folder(icon=None, item=None):
    subprocess.Popen(f'explorer "{APP_DIR}"')


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
            pystray.MenuItem("설정 폴더 열기", open_config_folder),
            pystray.MenuItem("종료", quit_app)
        )
    )

    icon.run()


if __name__ == "__main__":
    main()
