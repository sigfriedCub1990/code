from abc import ABC
import abc
from typing import override

from sqlalchemy.orm import Session

from .model import Batch


class AbstractRepository(ABC):
    @abc.abstractmethod
    def add(self, batch: Batch) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, reference: str) -> Batch:
        raise NotImplementedError

    @abc.abstractmethod
    def all(self) -> list[Batch]:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    _session: Session

    def __init__(self, session: Session):
        self._session = session

    @override
    def add(self, batch: Batch) -> None:
        self._session.add(batch)

    @override
    def get(self, reference: str) -> Batch:
        return (
            self._session.query(Batch)
            .where(
                Batch.reference == reference,
            )
            .scalar()
        )

    @override
    def all(self) -> list[Batch]:
        return self._session.query(Batch).all()
