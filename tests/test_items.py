"""Тесты функций карточки и операций с предметами."""

from datetime import date

import pytest

from items import (add_item, find_items, get_card_status, get_item_age,
                   is_valid_year, remove_item, sort_items)


def test_pr1_card_functions():
    current_year = date.today().year
    assert is_valid_year(2000, current_year)
    assert get_item_age(2000, current_year) == current_year - 2000
    assert get_card_status(
        "Рубль", "Россия", "Монета", 2000, current_year
    ) == "Карточка предмета готова."


def test_incomplete_card():
    assert get_card_status("Рубль", "Россия", "", 2000, 2026) == (
        "Добавьте описание предмета."
    )


def test_add_and_remove_item():
    items = []
    sections = [{"id": 1, "collection_id": 1, "name": "Россия"}]
    item = add_item(items, sections, 1, "Рубль", 2000, "Монета")
    assert item["id"] == 1
    remove_item(items, 1)
    assert items == []


def test_invalid_year_is_rejected():
    sections = [{"id": 1, "collection_id": 1, "name": "Россия"}]
    with pytest.raises(ValueError, match="год"):
        add_item([], sections, 1, "Рубль", date.today().year + 1, "Монета")


def test_duplicate_item_is_rejected():
    sections = [{"id": 1, "collection_id": 1, "name": "Россия"}]
    items = []
    add_item(items, sections, 1, "Рубль", 2000, "Монета")
    with pytest.raises(ValueError, match="уже есть"):
        add_item(items, sections, 1, "рубль", 2001, "Монета")


def test_find_and_sort_items():
    sections = [{"id": 1, "collection_id": 1, "name": "Россия"}]
    items = []
    add_item(items, sections, 1, "Японская монета", 2000, "Монета")
    add_item(items, sections, 1, "Альбом", 2001, "Альбом")
    assert [item["name"] for item in find_items(items, "МОНЕТА")] == [
        "Японская монета"
    ]
    assert [item["name"] for item in sort_items(items)] == [
        "Альбом", "Японская монета"
    ]
