from sqlalchemy import Column, ForeignKey, MetaData, String, Table, create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.types import Date, Integer

from .model import Batch, OrderLine


engine = create_engine("sqlite://", echo=True)

metadata = MetaData()


order_lines = Table(
    "order_lines",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("qty", Integer, nullable=False),
    Column("orderid", String(255)),
    Column("order_batch", Integer, ForeignKey("batches.id")),
)


batches = Table(
    "batches",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(255)),
    Column("reference", String(255)),
    Column("eta", Date, nullable=True),
    Column("_purchased_quantity", Integer, nullable=False),
)


class SessionFactory:
    @staticmethod
    def create_session():
        return sessionmaker(bind=engine)()


def start_mappers():
    mapper(OrderLine, order_lines)
    mapper(Batch, batches)


metadata.create_all(bind=engine)
start_mappers()
