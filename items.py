"""Карточки предметов и операции с ними."""

from datetime import date

from catalog import next_id


def is_valid_year(year: int, current_year: int) -> bool:
    """Проверить, что год предмета находится в допустимом диапазоне."""
    return 1 <= year <= current_year


def get_item_age(year: int, current_year: int) -> int:
    """Вернуть возраст предмета в годах."""
    return current_year - year


def get_card_status(
    name: str, section_name: str, description: str,
    year: int, current_year: int
) -> str:
    """Вернуть состояние карточки по заполненности обязательных полей."""
    if not name.strip() or not section_name.strip():
        return "Укажите название предмета и раздел."
    if not is_valid_year(year, current_year):
        return "Укажите корректный год предмета."
    if not description.strip():
        return "Добавьте описание предмета."
    return "Карточка предмета готова."


def add_item(
    items: list[dict], sections: list[dict], section_id: int,
    name: str, year: int, description: str
) -> dict:
    """Добавить предмет в существующий раздел."""
    if not any(section["id"] == section_id for section in sections):
        raise ValueError("Раздел не найден.")
    name = name.strip()
    if not name:
        raise ValueError("Название предмета не может быть пустым.")
    if not is_valid_year(year, date.today().year):
        raise ValueError("Некорректный год предмета.")
    if any(item["section_id"] == section_id and
           item["name"].casefold() == name.casefold() for item in items):
        raise ValueError("Предмет с таким названием уже есть в разделе.")
    item = {"id": next_id(items), "section_id": section_id, "name": name,
            "year": year, "description": description.strip()}
    items.append(item)
    return item


def remove_item(items: list[dict], item_id: int) -> None:
    """Удалить предмет по идентификатору."""
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
    """Вернуть предметы в алфавитном порядке."""
    return sorted(items, key=lambda item: item["name"].casefold())
