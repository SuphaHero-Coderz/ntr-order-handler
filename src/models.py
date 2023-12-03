from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from pydantic import Field as PyField


class UserCredentials(BaseModel):
    username: str
    password: str


class OrderCreate(BaseModel):
    user_id: int
    num_tokens: int
    user_credits: int
    order_fail: bool = PyField(default=False)
    payment_fail: bool = PyField(default=False)
    inventory_fail: bool = PyField(default=False)
    delivery_fail: bool = PyField(default=False)


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    status: Optional[str] = Field(default="processing")
    status_message: Optional[str] = Field(default="Order created")
    last_updated: Optional[datetime] = Field(default=datetime.utcnow())
    created_at: Optional[datetime] = Field(default=datetime.utcnow())
