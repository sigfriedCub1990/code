from dataclasses import dataclass
from datetime import date
from typing import override


class OutOfStock(Exception):
    pass


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
        self.eta = eta
        self._purchased_quantity = quantity
        self._allocations = set()

    def allocate(self, order_line: OrderLine):
        if self.can_allocate(order_line):
            self._allocations.add(order_line)

    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

    def can_allocate(self, order_line: OrderLine):
        if order_line in self._allocations:
            return False

        return (
            self.sku == order_line.sku
            and self.available_quantity >= order_line.quantity
        )

    @property
    def available_quantity(self):
        return self._purchased_quantity - self.allocated_quantity

    @property
    def allocated_quantity(self):
        return sum(order.quantity for order in self._allocations)

    @override
    def __eq__(self, other: object):
        if not isinstance(other, Batch):
            return False
        return self.reference == other.reference

    @override
    def __hash__(self) -> int:
        return hash(self.reference)

    def __gt__(self, other: object):
        if not isinstance(other, Batch):
            raise TypeError("You must compare instances of Batch")

        if self.eta is None:
            return False
        if other.eta is None:
            return True

        return self.eta > other.eta


def allocate(line: OrderLine, batches: list[Batch]) -> str:
    try:
        batch = next(b for b in sorted(batches) if b.can_allocate(line))
        batch.allocate(line)

        return batch.reference
    except StopIteration:
        raise OutOfStock(f"Out of stock for sku {line.sku}")
