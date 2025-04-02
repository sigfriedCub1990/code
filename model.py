from dataclasses import dataclass
from datetime import date


@dataclass(kw_only=True, frozen=True)
class OrderLine:
    order_reference: str
    sku: str
    quantity: int


class Batch:
    reference: str
    sku: str
    quantity: int
    eta: date | None
    _orders: list[str]

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
        self._orders = []

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self.quantity -= order_line.quantity
            self._orders.append(order_line.order_reference)

    def can_allocate(self, order_line: OrderLine):
        if order_line.order_reference in self._orders:
            return False

        return self.sku == order_line.sku and self.quantity >= order_line.quantity
