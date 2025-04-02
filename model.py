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
    eta: date | None
    _purchased_quantity: int
    _allocations: set[OrderLine]

    def __init__(
        self,
        reference: str,
        sku: str,
        quantity: int,
        eta: date | None = None,
    ):
        self.reference = reference
        self.sku = sku
        self._purchased_quantity = quantity
        self.eta = eta
        self._allocations = set()

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self):
        return sum(order.quantity for order in self._allocations)

    def can_allocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            return False

        return (
            self.sku == order_line.sku
            and self._purchased_quantity >= order_line.quantity
        )
