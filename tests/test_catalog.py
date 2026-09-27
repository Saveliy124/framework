"""Проверки операций с каталогом коллекций."""

import pytest

from catalog import (add_collection, add_item, add_owner, add_section,
                     collection_statistics, find_items, remove_item,
                     sort_items)


def make_catalog():
    """Создать небольшой каталог для независимых тестов."""
    owners, collections, sections, items = [], [], [], []
    owner = add_owner(owners, "Анна")
    collection = add_collection(collections, owners, owner["id"], "Монеты")
    section = add_section(sections, collections, collection["id"], "Россия")
    return owners, collections, sections, items, section


def test_add_item_and_statistics():
    _, collections, sections, items, section = make_catalog()
    add_item(items, sections, section["id"], "Рубль", "отличное", 100, True)
    stats = collection_statistics(1, collections, sections, items)
    assert stats == {"sections": 1, "items": 1, "estimated_value": 125.0}


def test_find_and_sort_items():
    _, _, sections, items, section = make_catalog()
    add_item(items, sections, section["id"], "Японская монета", "хорошее",
             50, False)
    add_item(items, sections, section["id"], "Альбом", "хорошее", 20, False)
    assert [item["name"] for item in find_items(items, "МОНЕТА")] == [
        "Японская монета"
    ]
    assert [item["name"] for item in sort_items(items)] == [
        "Альбом", "Японская монета"
    ]


def test_duplicate_item_is_rejected():
    _, _, sections, items, section = make_catalog()
    add_item(items, sections, section["id"], "Рубль", "хорошее", 100, False)
    with pytest.raises(ValueError):
        add_item(items, sections, section["id"], "рубль", "хорошее",
                 100, False)


def test_remove_item():
    _, _, sections, items, section = make_catalog()
    item = add_item(items, sections, section["id"], "Рубль", "хорошее",
                    100, False)
    remove_item(items, item["id"])
    assert items == []
