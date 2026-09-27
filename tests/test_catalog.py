"""Тесты связей и статистики каталога."""

import pytest

from catalog import (add_collection, add_owner, add_section,
                     collection_statistics)
from items import add_item


def test_catalog_hierarchy_and_statistics():
    owners, collections, sections, items = [], [], [], []
    owner = add_owner(owners, "Анна")
    collection = add_collection(collections, owners, owner["id"], "Монеты")
    section = add_section(sections, collections, collection["id"], "Россия")
    add_item(items, sections, section["id"], "Рубль", 2000, "Монета")
    assert collection_statistics(1, collections, sections, items) == {
        "sections": 1, "items": 1
    }


def test_collection_requires_owner():
    with pytest.raises(ValueError, match="Владелец не найден"):
        add_collection([], [], 42, "Монеты")
