from datetime import date, timedelta

from .model import Batch, OrderLine, allocate

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

    assert batch.available_quantity == 2


def test_trying_to_allocate_a_greater_quantity_than_available_does_nothing():
    batch, line = (
        Batch(reference="batch-001", sku="RED-CHAIR", quantity=10),
        OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=12),
    )

    batch.allocate(line)

    assert batch.available_quantity == 10


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


# This test is easy since we keep track of the
# allocated lines inside a Set (nice)
def test_allocate_is_idempotent():
    batch, line = make_batch_and_line(sku="RED-CHAIR", batch_qty=10, line_qty=2)

    batch.allocate(line)
    batch.allocate(line)

    assert batch.available_quantity == 8


def test_can_only_deallocate_allocated_lines():
    batch, line = make_batch_and_line(sku="RED-CHAIR", batch_qty=10, line_qty=8)

    batch.deallocate(line)

    assert batch.available_quantity == 10


def test_deallocating_an_allocated_line_increments_batch_quantity():
    batch, line = make_batch_and_line(sku="RED-CHAIR", batch_qty=10, line_qty=8)

    batch.allocate(line)

    assert batch.available_quantity == 2

    batch.deallocate(line)

    assert batch.available_quantity == 10


# def test_prefers_warehouse_batches_to_shipments():
#     pytest.fail("todo")


def test_prefers_earlier_batches():
    earliest = Batch(reference="speedy-batch", sku="RED-CHAIR", quantity=100, eta=today)
    medium = Batch(
        reference="speedy-batch", sku="RED-CHAIR", quantity=100, eta=tomorrow
    )
    latest = Batch(reference="speedy-batch", sku="RED-CHAIR", quantity=100, eta=later)
    line = OrderLine(order_reference="order-ref", sku="RED-CHAIR", quantity=10)

    allocate(line, [earliest, medium, latest])

    assert earliest.available_quantity == 90
    assert medium.available_quantity == 100
    assert latest.available_quantity == 100
