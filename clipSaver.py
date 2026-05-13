from pathlib import Path
from datetime import datetime
import threading
import subprocess
import sys
import re
import json

import pyperclip
import keyboard
import pystray
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import messagebox


BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "config.json"

DEFAULT_CONFIG = {
    "save_dir": "./",
    "hotkey": "ctrl+alt+a",
    "default_type": "ai-log",
    "default_tags": ["ai-log"],
    "preview_length": 300
}

last_saved = ""


def load_config():
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        merged = DEFAULT_CONFIG.copy()
        merged.update(config)
        return merged
    except Exception:
        return DEFAULT_CONFIG.copy()


def save_config(config):
    CONFIG_FILE.write_text(
        json.dumps(config, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def get_save_path():
    config = load_config()
    save_dir = config.get("save_dir", DEFAULT_CONFIG["save_dir"])

    path = Path(save_dir)

    if not path.is_absolute():
        path = BASE_DIR / path

    path.mkdir(parents=True, exist_ok=True)
    return path


def split_tags(value):
    value = value.replace("[", "").replace("]", "")
    value = value.replace('"', "").replace("'", "")
    return [tag.strip() for tag in re.split(r"[,/|]", value) if tag.strip()]


def normalize_tags(tags):
    result = []

    for tag in tags:
        tag = str(tag).strip().lower()
        tag = re.sub(r"^\s*[-*]\s*", "", tag)
        tag = re.sub(r"\s+", "-", tag)
        tag = re.sub(r"[^a-z0-9가-힣_-]", "", tag)

        if tag and tag not in result:
            result.append(tag)

    return result[:5]


def parse_ai_metadata(text, config):
    metadata = {
        "title": "",
        "summary": "",
        "tags": [],
        "type": config.get("default_type", "ai-log")
    }

    lines = text.splitlines()
    collecting_tags = False

    for raw_line in lines[:100]:
        line = raw_line.strip()

        if not line:
            continue

        if line in ("---", "```", "```markdown", "```md"):
            continue

        if line.startswith("```"):
            continue

        key_match = re.match(
            r"^(title|summary|type)\s*:\s*(.*?)\s*$",
            line,
            re.IGNORECASE
        )

        if key_match:
            key = key_match.group(1).lower()
            value = key_match.group(2).strip().strip('"').strip("'")

            if value:
                metadata[key] = value

            collecting_tags = False
            continue

        tags_start = re.match(
            r"^tags\s*:\s*(.*?)\s*$",
            line,
            re.IGNORECASE
        )

        if tags_start:
            collecting_tags = True
            inline_value = tags_start.group(1).strip()

            if inline_value:
                metadata["tags"].extend(split_tags(inline_value))

            continue

        if collecting_tags:
            nested_key = re.match(
                r"^(title|summary|type)\s*:\s*(.*?)\s*$",
                line,
                re.IGNORECASE
            )

            if nested_key:
                key = nested_key.group(1).lower()
                value = nested_key.group(2).strip().strip('"').strip("'")

                if value:
                    metadata[key] = value

                collecting_tags = False
                continue

            tag_match = re.match(r"^[-*]\s+(.+?)\s*$", line)

            if tag_match:
                metadata["tags"].append(tag_match.group(1).strip())
                continue

            plain_tag_match = re.match(
                r"^[a-zA-Z0-9가-힣][a-zA-Z0-9가-힣_-]*$",
                line
            )

            if plain_tag_match:
                metadata["tags"].append(line)
                continue

            collecting_tags = False

    metadata["tags"] = normalize_tags(metadata["tags"])

    if not metadata["tags"]:
        metadata["tags"] = normalize_tags(config.get("default_tags", ["ai-log"]))

    if not metadata["title"]:
        metadata["title"] = generate_title(text)

    if not metadata["summary"]:
        metadata["summary"] = generate_summary(text)

    return metadata


def generate_title(text):
    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line.startswith("---"):
            continue

        if line.startswith("#"):
            return line.lstrip("#").strip()[:60]

        if not re.match(r"^(title|summary|tags|type)\s*:", line, re.IGNORECASE):
            return line[:60]

    return "untitled-log"


def generate_summary(text):
    cleaned = []

    for line in text.splitlines():
        line = line.strip()

        if not line:
            continue

        if line in ("---", "```", "```markdown", "```md"):
            continue

        if re.match(r"^(title|summary|tags|type)\s*:", line, re.IGNORECASE):
            continue

        if re.match(r"^[-*]\s+", line):
            continue

        cleaned.append(line)

    if not cleaned:
        return "클립보드 내용을 저장한 메모."

    return " ".join(cleaned)[:120]


def remove_existing_metadata_block(text):
    lines = text.splitlines()

    if lines and lines[0].strip() == "---":
        for i in range(1, min(len(lines), 120)):
            if lines[i].strip() == "---":
                return "\n".join(lines[i + 1:]).strip()

    return text.strip()


def sanitize_filename(title):
    title = title.strip()
    title = re.sub(r'[\\/:*?"<>|]', "", title)
    title = re.sub(r"\s+", "-", title)
    return title[:80] or "untitled-log"


def build_markdown(metadata, body):
    tag_lines = "\n".join([f"  - {tag}" for tag in metadata.get("tags", [])])

    return f"""---
title: {metadata.get("title", "untitled-log")}
summary: {metadata.get("summary", "")}
tags:
{tag_lines}
type: {metadata.get("type", "ai-log")}
created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
---

{body}
"""


def create_icon_image():
    image = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(image)
    draw.ellipse((12, 12, 52, 52), fill="white")
    draw.text((24, 22), "A", fill="black")
    return image


def show_info(title, message):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    messagebox.showinfo(title, message)
    root.destroy()


def show_confirm_window(content: str) -> bool:
    config = load_config()
    preview_length = int(config.get("preview_length", 300))

    preview = content[:preview_length]

    if len(content) > preview_length:
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

    try:
        content = pyperclip.paste().strip()
        config = load_config()

        if not content:
            show_info("Clip Saver", "클립보드가 비어있어.")
            return

        if content == last_saved:
            show_info("Clip Saver", "이미 저장한 내용이야.")
            return

        if not show_confirm_window(content):
            return

        metadata = parse_ai_metadata(content, config)
        body = remove_existing_metadata_block(content)

        now = datetime.now()
        filename = f"{now.strftime('%Y-%m-%d_%H%M%S')}_{sanitize_filename(metadata['title'])}.md"

        save_path = get_save_path()
        path = save_path / filename

        md = build_markdown(metadata, body)
        path.write_text(md, encoding="utf-8")

        last_saved = content

        show_info("Clip Saver", f"저장 완료\n\n{path}")

    except Exception as e:
        show_info("Clip Saver 오류", str(e))


def open_save_folder(icon=None, item=None):
    save_path = get_save_path()
    subprocess.Popen(f'explorer "{save_path}"')


def quit_app(icon, item):
    keyboard.unhook_all_hotkeys()
    icon.stop()
    sys.exit()


def register_hotkey():
    config = load_config()
    hotkey = config.get("hotkey", DEFAULT_CONFIG["hotkey"])
    keyboard.add_hotkey(hotkey, save_clipboard)


def main():
    get_save_path()
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