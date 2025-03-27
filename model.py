from dataclasses import dataclass


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

    def decrement(self, quantity: int):
        self.quantity -= quantity


class Allocator:
    def __init__(self, batches: list[Batch]) -> None:
        self.batches = batches

    def allocate(self, batch: Batch) -> None:
        [current_batch] = filter(lambda b: b.reference == batch.reference, self.batches)

        current_batch.decrement(batch.quantity)

    def get_batch(self, reference: str):
        [current_batch] = filter(
            lambda batch: batch.reference == reference, self.batches
        )

        return current_batch
