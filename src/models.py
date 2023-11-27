import enum

from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class OrderInformation(BaseModel):
    num_tokens: int


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    payment_status: Optional[bool] = Field(default=False)
    delivery_status: Optional[bool] = Field(default=False)
    created_at: Optional[datetime] = Field(default=datetime.utcnow())
