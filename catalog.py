"""Функции для работы с каталогами коллекций."""

from valuation import calculate_estimated_value, get_condition_multiplier


def next_id(records: list[dict]) -> int:
    """Вернуть следующий идентификатор для списка записей."""
    return max((record["id"] for record in records), default=0) + 1


def add_owner(owners: list[dict], name: str) -> dict:
    """Добавить владельца и вернуть созданную запись."""
    name = name.strip()
    if not name:
        raise ValueError("Имя владельца не может быть пустым.")
    owner = {"id": next_id(owners), "name": name}
    owners.append(owner)
    return owner


def add_collection(
    collections: list[dict], owners: list[dict], owner_id: int, name: str
) -> dict:
    """Добавить коллекцию существующего владельца."""
    name = name.strip()
    if not any(owner["id"] == owner_id for owner in owners):
        raise ValueError("Владелец не найден.")
    if not name:
        raise ValueError("Название коллекции не может быть пустым.")
    collection = {"id": next_id(collections), "owner_id": owner_id,
                  "name": name}
    collections.append(collection)
    return collection


def add_section(
    sections: list[dict], collections: list[dict],
    collection_id: int, name: str
) -> dict:
    """Добавить раздел существующей коллекции."""
    name = name.strip()
    if not any(item["id"] == collection_id for item in collections):
        raise ValueError("Коллекция не найдена.")
    if not name:
        raise ValueError("Название раздела не может быть пустым.")
    section = {"id": next_id(sections), "collection_id": collection_id,
               "name": name}
    sections.append(section)
    return section


def add_item(
    items: list[dict], sections: list[dict], section_id: int,
    name: str, condition: str, base_price: float,
    has_certificate: bool
) -> dict:
    """Добавить предмет в существующий раздел."""
    name = name.strip()
    if not any(section["id"] == section_id for section in sections):
        raise ValueError("Раздел не найден.")
    if not name:
        raise ValueError("Название предмета не может быть пустым.")
    if base_price < 0:
        raise ValueError("Цена не может быть отрицательной.")
    if any(item["section_id"] == section_id and
           item["name"].casefold() == name.casefold() for item in items):
        raise ValueError("Предмет с таким названием уже есть в разделе.")
    item = {"id": next_id(items), "section_id": section_id, "name": name,
            "condition": condition.strip(), "base_price": base_price,
            "has_certificate": has_certificate}
    items.append(item)
    return item


def remove_item(items: list[dict], item_id: int) -> None:
    """Удалить предмет по идентификатору или сообщить об ошибке."""
    for item in items:
        if item["id"] == item_id:
            items.remove(item)
            return
    raise ValueError("Предмет не найден.")


def find_items(items: list[dict], query: str) -> list[dict]:
    """Найти предметы по части названия без учёта регистра."""
    return [item for item in items
            if query.casefold() in item["name"].casefold()]


def sort_items(items: list[dict]) -> list[dict]:
    """Вернуть предметы по алфавиту, не меняя исходный список."""
    return sorted(items, key=lambda item: item["name"].casefold())


def collection_statistics(
    collection_id: int, collections: list[dict],
    sections: list[dict], items: list[dict]
) -> dict:
    """Подсчитать разделы, предметы и их предварительную стоимость."""
    if not any(item["id"] == collection_id for item in collections):
        raise ValueError("Коллекция не найдена.")
    section_ids = {section["id"] for section in sections
                   if section["collection_id"] == collection_id}
    collection_items = [item for item in items
                        if item["section_id"] in section_ids]
    total_value = sum(
        calculate_estimated_value(
            item["base_price"], get_condition_multiplier(item["condition"])
        ) for item in collection_items
    )
    return {"sections": len(section_ids), "items": len(collection_items),
            "estimated_value": round(total_value, 2)}
