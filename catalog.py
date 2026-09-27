"""Владельцы, коллекции и разделы каталога."""


def next_id(records: list[dict]) -> int:
    """Вернуть следующий свободный идентификатор записи."""
    return max((record["id"] for record in records), default=0) + 1


def add_owner(owners: list[dict], name: str) -> dict:
    """Добавить владельца в список."""
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
    if not any(owner["id"] == owner_id for owner in owners):
        raise ValueError("Владелец не найден.")
    name = name.strip()
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
    if not any(item["id"] == collection_id for item in collections):
        raise ValueError("Коллекция не найдена.")
    name = name.strip()
    if not name:
        raise ValueError("Название раздела не может быть пустым.")
    section = {"id": next_id(sections), "collection_id": collection_id,
               "name": name}
    sections.append(section)
    return section


def collection_statistics(
    collection_id: int, collections: list[dict],
    sections: list[dict], items: list[dict]
) -> dict:
    """Подсчитать разделы и предметы выбранной коллекции."""
    if not any(item["id"] == collection_id for item in collections):
        raise ValueError("Коллекция не найдена.")
    section_ids = {section["id"] for section in sections
                   if section["collection_id"] == collection_id}
    item_count = sum(item["section_id"] in section_ids for item in items)
    return {"sections": len(section_ids), "items": item_count}
