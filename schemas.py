from pydantic import BaseModel, Field


class Party(BaseModel):
    name: str
    bin_iin: str = Field(min_length=12, max_length=12)
    amount: int = Field(gt=0)


class LineItem(BaseModel):
    description: str
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class Invoice(BaseModel):
    invoice_number: str
    supplier: Party
    line_items: list[LineItem]
    total_amount: float = Field(gt=0)


invoice_data = {
    "invoice_number": "ЭСФ-2026-001",
    "supplier": {
        "name": "ТОО 'Kaspi Магазин'",
        "bin_iin": "123456789012",
        "amount": 50000,
    },
    "line_items": [
        {"description": "Ноутбук Lenovo", "quantity": 2, "price": 300000},
        {"description": "Мышка беспроводная", "quantity": 1, "price": 10000},
    ],
    "total_amount": 620000,
}

# # 1. Правильные данные
# raw_data = {
#     "name": "ТОО 'Kaspi Магазин'",
#     "bin_iin": "123456789012",
#     "amount": "50000",
# }

# clean_party = Party(**raw_data)
# print("✅ Правильные данные прошли:", clean_party)


# # 2. Плохие данные (ловим ошибку красиво через try / except)
# bad_data = {
#     "name": "ТОО 'Kaspi Магазин'",
#     "bin_iin": "1234012",
#     "amount": "-5000",
# }

# try:
#     clean_party_1 = Party(**bad_data)
# except ValidationError as e:
#     print("❌ Ошибка валидации данных:", e)
#     print(e)


clean_invoice = Invoice(**invoice_data)
print("✅ Счёт полностью проверен!")
print(f"Номер счёта: {clean_invoice.invoice_number}")
print(
    f"Продавец: {clean_invoice.supplier.name} (БИН: {clean_invoice.supplier.bin_iin})"
)
print(f"Количество позиций в чеке: {len(clean_invoice.line_items)}")
print(f"Первый товар: {clean_invoice.line_items[0].description}")
print(f"Итого к оплате: {clean_invoice.total_amount} тенге")

# Считаем сумму всех позиций: (количество * цена) для каждого товара
total_calculated = sum(item.quantity * item.price for item in clean_invoice.line_items)
# --- ПРОВЕРКА МАТЕМАТИКИ СЧЕТА ---
total_calculated = sum(item.quantity * item.price for item in clean_invoice.line_items)

print(f"\nСумма по позициям (расчетная): {total_calculated}")
print(f"Сумма, указанная в чеке: {clean_invoice.total_amount}")

if total_calculated == clean_invoice.total_amount:
    print("🎯 Математика сошлась! Никто не ошибся.")
else:
    print(
        f"🚨 Внимание! Расхождение на {abs(clean_invoice.total_amount - total_calculated)} тенге!"
    )
