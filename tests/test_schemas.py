import pytest
from pydantic import ValidationError

from schemas import Invoice, Party


# 1. Проверяем корректное создание контрагента
def test_valid_party_creation():
    data = {
        "name": "ТОО 'Kaspi Магазин'",
        "bin_iin": "123456789012",
        "amount": 50000,
    }
    party = Party(**data)

    assert party.name == "ТОО 'Kaspi Магазин'"
    assert party.bin_iin == "123456789012"
    assert party.amount == 50000


# 2. Проверяем валидацию БИН (должно упасть при длине не 12 символов)
def test_invalid_bin_raises_error():
    bad_data = {
        "name": "ТОО 'Kaspi Магазин'",
        "bin_iin": "12345",
        "amount": 50000,
    }
    with pytest.raises(ValidationError):
        Party(**bad_data)


# 3. Проверяем валидность структуры полного счета
def test_valid_invoice_creation():
    invoice_data = {
        "invoice_number": "ЭСФ-2026-001",
        "supplier": {
            "name": "ТОО 'Kaspi Магазин'",
            "bin_iin": "123456789012",
            "amount": 50000,
        },
        "line_items": [
            {"description": "Ноутбук Lenovo", "quantity": 2, "price": 300000.0},
            {"description": "Мышка беспроводная", "quantity": 1, "price": 10000.0},
        ],
        "total_amount": 610000.0,
    }

    invoice = Invoice(**invoice_data)
    assert invoice.invoice_number == "ЭСФ-2026-001"
    assert len(invoice.line_items) == 2

    # Проверка математики позиций внутри теста
    calculated_total = sum(item.quantity * item.price for item in invoice.line_items)
    assert calculated_total == invoice.total_amount
