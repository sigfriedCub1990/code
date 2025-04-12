import pytest
from sqlalchemy.orm import Session

from .model import Batch, OrderLine

from .repository import SqlAlchemyRepository


def insert_allocation(session: Session, orderline_id: int, batch_id: int):
    session.execute(
        "INSERT INTO allocations (orderline_id, batch_id)"
        + " VALUES (:orderline_id, :batch_id)",
        dict(orderline_id=orderline_id, batch_id=batch_id),
    )


@pytest.fixture
def order_line(session: Session) -> int:
    order_line = OrderLine(
        orderid="order1",
        sku="ROLLERCOASTER",
        qty=10,
    )
    session.add(order_line)
    session.commit()

    return order_line.id


@pytest.fixture
def batch(session: Session) -> Batch:
    batch = Batch(
        ref="batch4",
        sku="ROLLERCOASTER",
        qty=100,
        eta=None,
    )
    session.add(batch)
    session.commit()

    return batch


def test_repository_can_save_a_batch(session: Session):
    batch = Batch(
        ref="batch1",
        sku="RUSTY-SOAPDISH",
        qty=100,
        eta=None,
    )

    repo = SqlAlchemyRepository(session)
    repo.add(batch)
    session.commit()

    rows = session.execute(
        'select reference, sku, _purchased_quantity, eta from "batches"'
    )

    assert list(rows) == [("batch1", "RUSTY-SOAPDISH", 100, None)]


def test_repository_can_retrieve_a_batch(session: Session):
    batch = Batch(ref="batch2", sku="RED-CHAIR", qty=10, eta=None)
    session.add(batch)
    session.commit()

    repo = SqlAlchemyRepository(session)
    row = repo.get("batch2")

    assert row == Batch(
        ref="batch2",
        sku="RUSTY-SOAPDISH",
        qty=100,
        eta=None,
    )


def test_repository_can_retrieve_a_batch_with_allocations(
    session: Session, order_line, batch
):
    insert_allocation(session, order_line, batch.id)

    repo = SqlAlchemyRepository(session)
    retrieved = repo.get("batch4")

    expected = Batch(
        ref="batch4",
        sku="ROLLERCOASTER",
        qty=100,
        eta=None,
    )

    assert retrieved == expected

    assert retrieved.sku == expected.sku
    assert retrieved._purchased_quantity == expected._purchased_quantity
    assert retrieved._allocations == {
        OrderLine(
            orderid="order1",
            sku="ROLLERCOASTER",
            qty=10,
        )
    }
