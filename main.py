"""Консольное меню сервиса каталогов коллекций."""

from datetime import date
from pathlib import Path

from catalog import (add_collection, add_owner, add_section,
                     collection_statistics)
from items import (add_item, find_items, get_card_status, get_item_age,
                   is_valid_year, remove_item, sort_items)
from storage import load_data, save_data
from utils import input_int


DATA_DIR = Path(__file__).parent / "data"
DATA_FILES = {name: DATA_DIR / f"{name}.json" for name in
              ("owners", "collections", "sections", "items")}


def find_record(records: list[dict], record_id: int, title: str) -> dict:
    """Найти запись по ID или сообщить об отсутствии."""
    for record in records:
        if record["id"] == record_id:
            return record
    raise ValueError(f"{title} не найден.")


def show_catalog(data: dict[str, list[dict]]) -> None:
    """Вывести каталог по владельцам, коллекциям и разделам."""
    if not data["owners"]:
        print("Каталог пуст.")
        return
    for owner in data["owners"]:
        print(f'Владелец {owner["id"]}: {owner["name"]}')
        for collection in data["collections"]:
            if collection["owner_id"] != owner["id"]:
                continue
            print(f'  Коллекция {collection["id"]}: {collection["name"]}')
            for section in data["sections"]:
                if section["collection_id"] != collection["id"]:
                    continue
                print(f'    Раздел {section["id"]}: {section["name"]}')
                for item in data["items"]:
                    if item["section_id"] == section["id"]:
                        print(f'      Предмет {item["id"]}: {item["name"]}')


def show_item_card(data: dict[str, list[dict]], item_id: int) -> None:
    """Показать карточку предмета с данными его раздела и владельца."""
    item = find_record(data["items"], item_id, "Предмет")
    section = find_record(data["sections"], item["section_id"], "Раздел")
    collection = find_record(
        data["collections"], section["collection_id"], "Коллекция"
    )
    owner = find_record(data["owners"], collection["owner_id"], "Владелец")
    current_year = date.today().year
    status = get_card_status(
        item["name"], section["name"], item["description"],
        item["year"], current_year
    )

    print("\nКарточка предмета")
    print(f'Владелец: {owner["name"]}')
    print(f'Коллекция: {collection["name"]}')
    print(f'Раздел: {section["name"]}')
    print(f'Предмет: {item["name"]}')
    print(f'Год: {item["year"]}')
    if is_valid_year(item["year"], current_year):
        print(f'Возраст: {get_item_age(item["year"], current_year)} лет')
    print(f'Описание: {item["description"] or "не указано"}')
    print(status)


def show_items(items: list[dict]) -> None:
    """Вывести краткий список предметов."""
    if not items:
        print("Предметы не найдены.")
    for item in items:
        print(f'Предмет {item["id"]}: {item["name"]} '
              f'(раздел {item["section_id"]})')


def main() -> None:
    """Загрузить данные и выполнять действия меню до выхода."""
    try:
        data = {name: load_data(filename)
                for name, filename in DATA_FILES.items()}
    except (ValueError, OSError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    while True:
        print("\n=== Каталоги коллекций ===")
        print("1. Показать каталог")
        print("2. Показать карточку предмета")
        print("3. Добавить владельца")
        print("4. Добавить коллекцию")
        print("5. Добавить раздел")
        print("6. Добавить предмет")
        print("7. Удалить предмет")
        print("8. Найти предмет")
        print("9. Показать предметы по алфавиту")
        print("10. Статистика коллекции")
        print("0. Выход")

        try:
            choice = input("Выберите действие: ").strip()
            changed = None
            message = None
            if choice == "0":
                return
            elif choice == "1":
                show_catalog(data)
            elif choice == "2":
                show_item_card(data, input_int("ID предмета: "))
            elif choice == "3":
                owner = add_owner(data["owners"], input("Имя владельца: "))
                changed = "owners"
                message = f'Добавлен владелец с ID {owner["id"]}.'
            elif choice == "4":
                owner_id = input_int("ID владельца: ")
                name = input("Название коллекции: ")
                collection = add_collection(
                    data["collections"], data["owners"], owner_id, name
                )
                changed = "collections"
                message = f'Добавлена коллекция с ID {collection["id"]}.'
            elif choice == "5":
                collection_id = input_int("ID коллекции: ")
                name = input("Название раздела: ")
                section = add_section(
                    data["sections"], data["collections"],
                    collection_id, name
                )
                changed = "sections"
                message = f'Добавлен раздел с ID {section["id"]}.'
            elif choice == "6":
                section_id = input_int("ID раздела: ")
                name = input("Название предмета: ")
                year = input_int("Год предмета: ")
                description = input("Описание: ")
                item = add_item(
                    data["items"], data["sections"], section_id,
                    name, year, description
                )
                changed = "items"
                message = f'Добавлен предмет с ID {item["id"]}.'
            elif choice == "7":
                remove_item(data["items"], input_int("ID предмета: "))
                changed = "items"
                message = "Предмет удалён."
            elif choice == "8":
                show_items(find_items(data["items"],
                                      input("Часть названия: ")))
            elif choice == "9":
                show_items(sort_items(data["items"]))
            elif choice == "10":
                collection_id = input_int("ID коллекции: ")
                stats = collection_statistics(
                    collection_id, data["collections"],
                    data["sections"], data["items"]
                )
                print(f'Разделов: {stats["sections"]}; '
                      f'предметов: {stats["items"]}.')
            else:
                print("Неизвестное действие.")
            if changed is not None:
                save_data(DATA_FILES[changed], data[changed])
                print(message)
        except (ValueError, OSError) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            return


if __name__ == "__main__":
    main()
