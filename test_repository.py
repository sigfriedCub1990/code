from sqlalchemy.orm import Session

from .model import Batch

from .repository import SqlAlchemyRepository


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
