from datetime import date, timedelta
import pytest

from .model import Batch, OrderLine

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def test_allocating_to_a_batch_reduces_the_available_quantity():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=8)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    batch.allocate(order_line)

    assert batch.quantity == 2


def test_trying_to_allocate_a_greater_quantity_than_available_does_nothing():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=12)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    batch.allocate(order_line)

    assert batch.quantity == 10


def test_can_allocate_if_available_greater_than_required():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=8)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    assert batch.can_allocate(order_line) is True


def test_cannot_allocate_if_available_smaller_than_required():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=12)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    assert batch.can_allocate(order_line) is False


def test_can_allocate_if_available_equal_to_required():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=10)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    assert batch.can_allocate(order_line) is True


def test_allocates_lines_with_same_sku():
    order_line = OrderLine(
        order_reference="order-ref", sku="TASTELESS-LAMP", quantity=10
    )
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    assert batch.can_allocate(order_line) is False


def test_can_not_allocate_order_line_twice():
    order_line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=2)
    order_line_2 = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=2)
    batch = Batch(reference="batch-1", sku="RED-CHAIR", quantity=10)

    batch.allocate(order_line)
    batch.allocate(order_line_2)

    assert batch.quantity == 8


# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")


# def test_prefers_earlier_batches():
#     pytest.fail("todo")
