"""Безопасный ввод чисел для консольного меню."""

from math import isfinite


def input_int(prompt: str) -> int:
    """Повторять запрос, пока пользователь не введёт целое число."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")


def input_price(prompt: str) -> float:
    """Повторять запрос, пока пользователь не введёт неотрицательную цену."""
    while True:
        try:
            price = float(input(prompt).replace(",", "."))
            if isfinite(price) and price >= 0:
                return price
        except ValueError:
            pass
        print("Введите неотрицательное число.")
