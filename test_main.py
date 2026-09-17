"""Тесты для начального сценария оценки коллекционных предметов."""

import unittest

from main import (
    calculate_estimated_value,
    calculate_service_fee,
    get_condition_multiplier,
    get_document_status,
)


class ValuationServiceTests(unittest.TestCase):
    """Проверки расчётов и статуса документов."""

    def test_multiplier_for_excellent_condition(self) -> None:
        self.assertEqual(get_condition_multiplier("отличное"), 1.25)

    def test_estimated_value(self) -> None:
        self.assertEqual(calculate_estimated_value(10000, 1.25), 12500)

    def test_fee_with_certificate(self) -> None:
        self.assertEqual(calculate_service_fee(12500, True), 625)

    def test_document_status(self) -> None:
        result = get_document_status(True, True)
        self.assertIn("подтверждены", result)


if __name__ == "__main__":
    unittest.main()
