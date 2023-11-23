import src.database as _database

from src.models import Order
from src.database import engine
from sqlmodel import Session


"""
DATABASE ZONE
"""


def create_database() -> None:
    """
    Initializes the database engine
    """
    _database.init_db()


"""
ORDER ZONE
"""


def create_order(order: Order):
    with Session(engine) as session:
        session.add(order)
        session.commit()