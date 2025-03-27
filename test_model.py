from datetime import date, timedelta
import pytest

from model import Allocator, Batch

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


@pytest.fixture
def batches():
    return [
        Batch(reference="first-batch", sku="RED-CHAIR", quantity=10),
        Batch(reference="second-batch", sku="TASTELESS-LAMP", quantity=1),
    ]


def test_allocating_to_a_batch_reduces_the_available_quantity(batches):
    allocator = Allocator(batches)

    batch = Batch(reference="first-batch", sku="RED-CHAIR", quantity=2)

    allocator.allocate(batch)

    assert allocator.get_batch(reference="first-batch") == Batch(
        reference="first-batch", sku="RED-CHAIR", quantity=8
    )


def test_can_allocate_if_available_greater_than_required():
    pytest.fail("todo")


def test_cannot_allocate_if_available_smaller_than_required():
    pytest.fail("todo")


def test_can_allocate_if_available_equal_to_required():
    pytest.fail("todo")


def test_prefers_warehouse_batches_to_shipments():
    pytest.fail("todo")


def test_prefers_earlier_batches():
    pytest.fail("todo")
