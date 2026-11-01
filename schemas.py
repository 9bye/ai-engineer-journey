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
