def calculate_price(base_price, condition):
    if condition == "отличное":
        return base_price * 1.2
    if condition == "хорошее":
        return base_price
    return base_price * 0.7

def calculate_fee(price):
    return price * 0.05


def get_document_status(has_document):
    if has_document == "да":
        return "Документ есть. Предмет можно передать эксперту."
    return "Документа нет. Нужно добавить описание предмета."


item_name = input("Название предмета: ")
base_price = float(input("Базовая цена, руб.: "))
condition = input("Состояние (отличное/хорошее/другое): ").lower()
has_document = input("Есть документ? (да/нет): ").lower()

price = calculate_price(base_price, condition)
fee = calculate_fee(price)
document_status = get_document_status(has_document)

print("\nРезультат оценки")
print("Предмет:", item_name)
print("Примерная цена:", price, "руб.")
print("Комиссия:", fee, "руб.")
print("Статус:", document_status)
