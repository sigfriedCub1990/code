from datetime import date, timedelta
import pytest

from .exceptions import CannotAllocateBatchException
from .model import Allocator, Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


@pytest.fixture
def batches() -> list[Batch]:
    return [
        Batch(reference="first-batch", sku="RED-CHAIR", quantity=10, eta=tomorrow),
        Batch(reference="second-batch", sku="TASTELESS-LAMP", quantity=1),
        Batch(reference="third-batch", sku="RED-CHAIR", quantity=10),
    ]


def test_allocating_to_a_batch_reduces_the_available_quantity(batches: list[Batch]):
    allocator = Allocator(batches)

    order_line = OrderLine(sku="RED-CHAIR", quantity=2)

    allocator.allocate(order_line)

    assert allocator.get_batch(reference="third-batch") == Batch(
        reference="third-batch", sku="RED-CHAIR", quantity=8
    )


def test_cannot_allocate_if_available_smaller_than_required(batches: list[Batch]):
    allocator = Allocator(batches)

    order_line = OrderLine(sku="RED-CHAIR", quantity=12)

    with pytest.raises(CannotAllocateBatchException):
        allocator.allocate(order_line)


def test_can_allocate_if_available_greater_than_required(batches: list[Batch]):
    allocator = Allocator(batches)

    order_line = OrderLine(sku="RED-CHAIR", quantity=6)

    allocator.allocate(order_line)

    assert allocator.get_batch(reference="third-batch") == Batch(
        reference="third-batch", sku="RED-CHAIR", quantity=4
    )


def test_can_allocate_if_available_equal_to_required(batches: list[Batch]):
    allocator = Allocator(batches)

    order_line = OrderLine(sku="RED-CHAIR", quantity=6)

    allocator.allocate(order_line)

    assert allocator.get_batch(reference="third-batch") == Batch(
        reference="third-batch", sku="RED-CHAIR", quantity=4
    )


def test_prefers_warehouse_batches_to_shipments(batches: list[Batch]):
    allocator = Allocator(batches)

    order_line = OrderLine(sku="RED-CHAIR", quantity=6)

    allocator.allocate(order_line)

    assert allocator.get_batch(reference="third-batch") == Batch(
        reference="third-batch",
        sku="RED-CHAIR",
        quantity=4,
        eta=None,
    )


def test_prefers_earlier_batches():
    pytest.fail("todo")
