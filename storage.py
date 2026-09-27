"""Загрузка и сохранение списков записей в JSON-файлах."""

import json
from pathlib import Path


def load_data(filename: Path) -> list[dict]:
    """Прочитать список словарей; отсутствующий файл считать пустым."""
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
    """Записать список словарей в JSON с русскими символами."""
    filename.parent.mkdir(parents=True, exist_ok=True)
    with filename.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
