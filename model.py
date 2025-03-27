from dataclasses import dataclass
from datetime import date

from .exceptions import CannotAllocateBatchException


@dataclass(kw_only=True)
class Customer:
    delivery_address: str


@dataclass(kw_only=True)
class Product:
    sku: str


@dataclass(kw_only=True)
class OrderLine:
    sku: str
    quantity: int


@dataclass(kw_only=True)
class Order:
    id: str
    lines: list[OrderLine]


@dataclass(kw_only=True)
class Batch:
    reference: str
    sku: str
    quantity: int
    eta: date | None = None

    def decrement(self, quantity: int):
        if quantity > self.quantity:
            raise CannotAllocateBatchException

        self.quantity -= quantity


class Allocator:
    def __init__(self, batches: list[Batch]) -> None:
        self.batches = batches

    def allocate(self, order_line: OrderLine) -> None:
        [current_batch, *tail] = filter(
            lambda b: b.sku == order_line.sku and b.eta is None,
            self.batches,
        )

        current_batch.decrement(order_line.quantity)

    def get_batch(self, reference: str):
        [current_batch] = filter(
            lambda batch: batch.reference == reference, self.batches
        )

        return current_batch
