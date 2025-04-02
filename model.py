from dataclasses import dataclass
from datetime import date


@dataclass(kw_only=True, frozen=True)
class OrderLine:
    sku: str
    quantity: int


class Batch:
    reference: str
    sku: str
    quantity: int
    eta: date | None

    def __init__(
        self, reference: str, sku: str, quantity: int, eta: date | None = None
    ):
        self.reference = reference
        self.sku = sku
        self.quantity = quantity
        self.eta = eta

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.quantity -= order_line.quantity

    def can_allocate(self, order_line: OrderLine):
        return self.sku == order_line.sku and self.quantity >= order_line.quantity
