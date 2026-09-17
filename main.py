"""Начальный сценарий сервиса оценки коллекционных предметов."""

from datetime import date


def get_condition_multiplier(item_condition: str) -> float:
    """Возвращает коэффициент стоимости в зависимости от состояния предмета."""
    normalized_condition = item_condition.strip().lower()

    if normalized_condition == "отличное":
        return 1.25
    if normalized_condition == "хорошее":
        return 1.0
    if normalized_condition == "удовлетворительное":
        return 0.7
    return 0.5


def calculate_estimated_value(base_price: float, multiplier: float) -> float:
    """Рассчитывает предварительную стоимость предмета."""
    return round(base_price * multiplier, 2)


def calculate_service_fee(estimated_value: float, has_certificate: bool) -> float:
    """Рассчитывает комиссию сервиса за проведение оценки."""
    if has_certificate:
        fee_rate = 0.05
    else:
        fee_rate = 0.08
    return round(estimated_value * fee_rate, 2)


def get_document_status(has_certificate: bool, expert_verified: bool) -> str:
    """Определяет статус документов по заявке на оценку."""
    if has_certificate and expert_verified:
        return "Документы подтверждены, можно оформить экспертное заключение."
    if has_certificate:
        return "Сертификат получен и ожидает проверки эксперта."
    return "Для экспертной оценки необходимо приложить сертификат или описание."


def run_evaluation() -> None:
    """Запускает консольный сценарий предварительной оценки одного предмета."""
    item_name = input("Название предмета: ").strip()
    base_price = float(input("Базовая цена, руб.: "))
    item_condition = input(
        "Состояние (отличное, хорошее, удовлетворительное, плохое): "
    )
    has_certificate = input("Есть сертификат? (да/нет): ").strip().lower() == "да"
    expert_name = input("Имя эксперта: ").strip()
    expert_verified = input("Эксперт проверил предмет? (да/нет): ").strip().lower() == "да"

    multiplier = get_condition_multiplier(item_condition)
    estimated_value = calculate_estimated_value(base_price, multiplier)
    service_fee = calculate_service_fee(estimated_value, has_certificate)
    document_status = get_document_status(has_certificate, expert_verified)
    evaluation_date = date.today()

    print("\nРезультат предварительной оценки")
    print(f"Предмет: {item_name}")
    print(f"Эксперт: {expert_name}")
    print(f"Дата оценки: {evaluation_date:%d.%m.%Y}")
    print(f"Коэффициент состояния: {multiplier}")
    print(f"Предварительная стоимость: {estimated_value:.2f} руб.")
    print(f"Комиссия сервиса: {service_fee:.2f} руб.")
    print(f"Статус документа: {document_status}")


if __name__ == "__main__":
    run_evaluation()
