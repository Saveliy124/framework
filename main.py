"""Начальный сценарий создания карточки предмета коллекции (ПР1)."""

from datetime import date


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


def run_item_card() -> None:
    """Собрать и показать карточку одного предмета без сохранения."""
    owner_name = input("Владелец: ").strip()
    collection_name = input("Коллекция: ").strip()
    section_name = input("Раздел: ").strip()
    item_name = input("Предмет: ").strip()
    year_text = input("Год предмета: ").strip()
    year = int(year_text) if year_text.isdigit() else 0
    description = input("Описание: ").strip()
    current_year = date.today().year

    print("\nКарточка предмета")
    print(f"Владелец: {owner_name}")
    print(f"Коллекция: {collection_name}")
    print(f"Раздел: {section_name}")
    print(f"Предмет: {item_name}")
    if is_valid_year(year, current_year):
        print(f"Возраст: {get_item_age(year, current_year)} лет")
    print(get_card_status(
        item_name, section_name, description, year, current_year
    ))


if __name__ == "__main__":
    run_item_card()
