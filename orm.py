from sqlalchemy import Column, ForeignKey, MetaData, String, Table, create_engine
from sqlalchemy.orm import mapper, relationship, sessionmaker
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

allocations = Table(
    "allocations",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("batch_id", ForeignKey("batches.id")),
    Column("order_id", ForeignKey("order_lines.id")),
)


class SessionFactory:
    @staticmethod
    def create_session():
        return sessionmaker(bind=engine)()


def start_mappers():
    lines_mapper = mapper(OrderLine, order_lines)
    mapper(
        Batch,
        batches,
        properties={
            "_allocations": relationship(
                lines_mapper,
                secondary=allocations,
                collection_class=set,
            )
        },
    )


metadata.create_all(bind=engine)
start_mappers()
