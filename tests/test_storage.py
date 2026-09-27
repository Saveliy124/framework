"""Проверки сохранения каталога в JSON."""

import pytest

from storage import load_data, save_data


def test_save_and_load_data(tmp_path):
    filename = tmp_path / "owners.json"
    owners = [{"id": 1, "name": "Анна"}]
    save_data(filename, owners)
    assert load_data(filename) == owners


def test_invalid_json_is_reported(tmp_path):
    filename = tmp_path / "items.json"
    filename.write_text("{broken", encoding="utf-8")
    with pytest.raises(ValueError, match="Некорректный JSON"):
        load_data(filename)
