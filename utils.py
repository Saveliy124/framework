"""Безопасный ввод целого числа."""


def input_int(prompt: str) -> int:
    """Повторять запрос до ввода целого числа."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введите целое число.")
