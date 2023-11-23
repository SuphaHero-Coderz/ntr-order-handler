import enum

from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrderStatus(enum.Enum):
    pending = 0
    payment = 1
    delivery = 2
    complete = 3
    failed = 4


class OrderInformation(BaseModel):
    num_tokens: int


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    payment_status: Optional[bool] = Field(default=False)
    delivery_status: Optional[bool] = Field(default=False)
    status: Optional[OrderStatus] = Field(default=OrderStatus.pending)
    created_at: Optional[datetime] = Field(default=datetime.utcnow())
