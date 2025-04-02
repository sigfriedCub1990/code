from datetime import date, timedelta
import pytest

from .model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_batch_and_line(sku: str, batch_qty: int, line_qty: int):
    return (
        Batch(reference="batch-001", sku=sku, quantity=batch_qty, eta=today),
        OrderLine(order_reference="order-ref", sku=sku, quantity=line_qty),
    )


def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_line(sku="RED-CHAIR", batch_qty=10, line_qty=8)

    batch.allocate(line)

    assert batch.quantity == 2


def test_trying_to_allocate_a_greater_quantity_than_available_does_nothing():
    batch, line = (
        Batch(reference="batch-001", sku="RED-CHAIR", quantity=10),
        OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=12),
    )

    batch.allocate(line)

    assert batch.quantity == 10


def test_can_allocate_if_available_greater_than_required():
    batch, line = (
        Batch(reference="batch-001", sku="RED-CHAIR", quantity=10),
        OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=8),
    )

    assert batch.can_allocate(line)


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = (
        Batch(reference="batch-001", sku="RED-CHAIR", quantity=10),
        OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=12),
    )

    assert batch.can_allocate(line) is False


def test_can_allocate_if_available_equal_to_required():
    batch, line = (
        Batch(reference="batch-001", sku="RED-CHAIR", quantity=10),
        OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=10),
    )

    assert batch.can_allocate(line)


def test_can_not_allocate_if_skus_dont_match():
    line = OrderLine(order_reference="order-ref", sku="TASTELESS-LAMP", quantity=10)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    assert batch.can_allocate(line) is False


def test_can_not_allocate_order_line_twice():
    line_1 = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=2)
    line_2 = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=2)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    batch.allocate(line_1)
    batch.allocate(line_2)

    assert batch.quantity == 8


# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")


# def test_prefers_earlier_batches():
#     pytest.fail("todo")
