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
    _order_lines: list[OrderLine]

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: date | None = None,
    ):
        self.reference = reference
        self.sku = sku
        self.quantity = quantity
        self.eta = eta
        self._order_lines = []

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.quantity -= order_line.quantity
            self._order_lines.append(order_line)

    def can_allocate(self, order_line: OrderLine):
        if order_line in self._order_lines:
            return False

        return self.sku == order_line.sku and self.quantity >= order_line.quantity
