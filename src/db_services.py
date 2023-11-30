import src.database as _database

from src.database import engine
from sqlmodel import Session, select
from src.models import Order, OrderCreate
from typing import List
from datetime import datetime

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


async def update_expired_orders() -> None:
    """
    Updates orders that have been processing for a set amount of time as failed
    due to timeout
    """
    with Session(engine) as session:
        query = select(Order)
        results: List[Order] = session.exec(query).all()

        for result in results:
            processing_time = (datetime.utcnow() - result.last_updated).total_seconds()
            if processing_time > 60 and result.status not in ["failed", "complete"]:
                result.status_message = "Order processing timed out"
                result.status = "failed"
                session.add(result)

        session.commit()

        for result in results:
            session.refresh(result)


async def create_order(order_info: OrderCreate, session: Session) -> Order:
    """
    Creates a new order object in the database

    Args:
        order_info (OrderCreate): order information
        session (Session): database session

    Returns:
        Order: the created order
    """
    order: Order = Order(
        user_id=order_info.user_id,
        num_tokens=order_info.num_tokens,
    )

    session.add(order)
    session.commit()

    return order


async def get_orders(user_id: int, session: Session) -> List[Order]:
    """
    Gets orders for user with `user_id`

    Args:
        user_id (int): the id of the user to query
        session (Session): database session

    Returns:
        List[Order]: orders of the user
    """
    query = select(Order).where(Order.user_id == user_id)
    results: List[Order] = session.exec(query).all()

    return results


async def get_all_orders(session: Session) -> List[Order]:
    """
    Gets ALL orders of ALL users

    Args:
        session (Session): database session

    Returns:
        List[Order]: list of all orders
    """
    query = select(Order)
    results: List[Order] = session.exec(query).all()

    return results


async def update_order_status(
    order_id: int, status: str, status_message: str, session: Session
):
    """
    Updates the status of an order

    Args:
        order_id (int): order id to update
        status (str): order status
        status_message (str): corresponding status message
        session (Session): database session
    """
    query = select(Order).where(Order.id == order_id)
    result: Order = session.exec(query).one()

    result.status = status
    result.status_message = status_message
    result.last_updated = datetime.utcnow()

    session.add(result)
    session.commit()
