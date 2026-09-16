from decimal import Decimal
from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict

# Современный способ объявления типов с ограничениями в V2:
PositiveDecimal = Annotated[Decimal, Field(gt=0)]
TransactionTypeStr = Annotated[str, Field(pattern="^(debit|credit)$")]
CurrencyStr = Annotated[str, Field(min_length=3, max_length=3)]

class Transaction(BaseModel):
    amount: PositiveDecimal
    transaction_type: TransactionTypeStr
    currency: CurrencyStr

    # Новый синтаксис конфигурации
    model_config = ConfigDict(
        str_strip_whitespace=True  # Новое имя для anystr_strip_whitespace
    )

# Пример транзакции
transaction = Transaction(amount=150.50, transaction_type="debit", currency="USD")
print(transaction)
