import enum

from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrderStatus(enum.Enum):
    created = 0
    payment = 1
    delivery = 2
    complete = 3


class UserCredentials(BaseModel):
    username: str
    password: str


class OrderCreate(BaseModel):
    user_id: int
    num_tokens: int


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    status: Optional[OrderStatus] = Field(default=OrderStatus.created)
    created_at: Optional[datetime] = Field(default=datetime.utcnow())
