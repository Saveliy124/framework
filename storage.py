"""Загрузка и сохранение списков записей в JSON."""

import json
from pathlib import Path


def load_data(filename: Path) -> list[dict]:
    """Загрузить записи; отсутствующий файл считать пустым списком."""
    try:
        with filename.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(f"Некорректный JSON в файле {filename}.") from error
    if not isinstance(data, list) or not all(
        isinstance(record, dict) for record in data
    ):
        raise ValueError(f"Ожидался список записей в файле {filename}.")
    return data


def save_data(filename: Path, data: list[dict]) -> None:
    """Сохранить записи в JSON с поддержкой русских символов."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
