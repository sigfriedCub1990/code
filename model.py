from dataclasses import dataclass
from datetime import date

from .exceptions import CannotAllocateBatchException


@dataclass(kw_only=True)
class OrderLine:
    sku: str
    quantity: int


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


class BatchList(list[Batch]):
    def warehouse_batches(self):
        return BatchList(list(filter(lambda b: b.eta is None, self)))

    def shipment_batches(self):
        return BatchList(list(filter(lambda b: b.eta is not None, self)))

    def get_by_sku(self, sku: str):
        return BatchList(list(filter(lambda b: b.sku == sku, self)))

    def sort_by_eta(self):
        return BatchList(sorted(self, key=lambda batch: batch.eta or ""))

    def first(self):
        if self:
            return self[0]
        return None


class Allocator:
    def __init__(self, batches: list[Batch]) -> None:
        self.batches: BatchList = BatchList(batches)

    def allocate(self, order_line: OrderLine) -> None:
        available_batches = self.batches.get_by_sku(order_line.sku)

        warehouse_batches = available_batches.warehouse_batches().first()

        if warehouse_batches:
            warehouse_batches.decrement(order_line.quantity)
            return

        due_batch = available_batches.shipment_batches().sort_by_eta().first()

        if due_batch:
            due_batch.decrement(order_line.quantity)

    def get_batch(self, reference: str):
        [current_batch] = filter(
            lambda batch: batch.reference == reference, self.batches
        )

        return current_batch
