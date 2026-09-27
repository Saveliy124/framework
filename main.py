"""Консольное меню сервиса каталогов коллекций."""

from pathlib import Path

from catalog import (add_collection, add_item, add_owner, add_section,
                     collection_statistics, find_items, remove_item,
                     sort_items)
from storage import load_data, save_data
from utils import input_int, input_price
from valuation import run_evaluation


DATA_DIR = Path(__file__).parent / "data"
DATA_FILES = {name: DATA_DIR / f"{name}.json" for name in
              ("owners", "collections", "sections", "items")}


def show_catalog(data: dict[str, list[dict]]) -> None:
    """Вывести владельцев, их коллекции, разделы и предметы."""
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


def show_items(items: list[dict]) -> None:
    """Вывести краткий список найденных или отсортированных предметов."""
    if not items:
        print("Предметы не найдены.")
    for item in items:
        print(f'Предмет {item["id"]}: {item["name"]} '
              f'(раздел {item["section_id"]})')


def main() -> None:
    """Загрузить каталог и выполнять выбранные действия до выхода."""
    try:
        data = {name: load_data(filename)
                for name, filename in DATA_FILES.items()}
    except (ValueError, OSError) as error:
        print(f"Не удалось загрузить данные: {error}")
        return

    while True:
        print("\n=== Каталоги коллекций ===")
        print("1. Показать каталог")
        print("2. Добавить владельца")
        print("3. Добавить коллекцию")
        print("4. Добавить раздел")
        print("5. Добавить предмет")
        print("6. Удалить предмет")
        print("7. Найти предмет")
        print("8. Показать предметы по алфавиту")
        print("9. Статистика коллекции")
        print("10. Оценить предмет (сценарий ПР1)")
        print("0. Выход")

        try:
            choice = input("Выберите действие: ").strip()
            changed = None
            if choice == "0":
                return
            elif choice == "1":
                show_catalog(data)
            elif choice == "2":
                owner = add_owner(data["owners"], input("Имя владельца: "))
                changed = "owners"
                print(f'Добавлен владелец с ID {owner["id"]}.')
            elif choice == "3":
                owner_id = input_int("ID владельца: ")
                name = input("Название коллекции: ")
                collection = add_collection(
                    data["collections"], data["owners"], owner_id, name
                )
                changed = "collections"
                print(f'Добавлена коллекция с ID {collection["id"]}.')
            elif choice == "4":
                collection_id = input_int("ID коллекции: ")
                name = input("Название раздела: ")
                section = add_section(
                    data["sections"], data["collections"],
                    collection_id, name
                )
                changed = "sections"
                print(f'Добавлен раздел с ID {section["id"]}.')
            elif choice == "5":
                section_id = input_int("ID раздела: ")
                name = input("Название предмета: ")
                condition = input("Состояние предмета: ")
                base_price = input_price("Базовая цена, руб.: ")
                has_certificate = (
                    input("Есть сертификат? (да/нет): ").strip().lower()
                    == "да"
                )
                item = add_item(
                    data["items"], data["sections"], section_id,
                    name, condition, base_price, has_certificate
                )
                changed = "items"
                print(f'Добавлен предмет с ID {item["id"]}.')
            elif choice == "6":
                remove_item(data["items"], input_int("ID предмета: "))
                changed = "items"
                print("Предмет удалён.")
            elif choice == "7":
                show_items(find_items(data["items"],
                                      input("Часть названия: ")))
            elif choice == "8":
                show_items(sort_items(data["items"]))
            elif choice == "9":
                collection_id = input_int("ID коллекции: ")
                stats = collection_statistics(
                    collection_id, data["collections"],
                    data["sections"], data["items"]
                )
                print(f'Разделов: {stats["sections"]}; '
                      f'предметов: {stats["items"]}; '
                      f'стоимость: {stats["estimated_value"]:.2f} руб.')
            elif choice == "10":
                run_evaluation()
            else:
                print("Неизвестное действие.")
            if changed is not None:
                save_data(DATA_FILES[changed], data[changed])
        except (ValueError, OSError) as error:
            print(f"Ошибка: {error}")
        except (EOFError, KeyboardInterrupt):
            print("\nВыход.")
            return


if __name__ == "__main__":
    main()
