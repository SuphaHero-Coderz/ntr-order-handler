import src.database as _database

from sqlmodel import Session, select
from src.models import Order, OrderCreate
from typing import List

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


async def create_order(order_info: OrderCreate, session: Session) -> Order:
    order: Order = Order(
        user_id=order_info.user_id,
        num_tokens=order_info.num_tokens,
    )

    session.add(order)
    session.commit()

    return order


async def get_orders(user_id: int, session: Session) -> List[Order]:
    query = select(Order).where(Order.user_id == user_id)
    results: List[Order] = session.exec(query).all()

    return results


async def update_order_status(order_id: int, status: str, session: Session):
    query = select(Order).where(Order.id == order_id)
    result: Order = session.exec(query).one()

    result.status = status

    session.add(result)
    session.commit()
