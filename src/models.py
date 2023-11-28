from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class UserCredentials(BaseModel):
    username: str
    password: str


class OrderCreate(BaseModel):
    user_id: int
    num_tokens: int
    user_credits: int


class Order(SQLModel, table=True):
    __tablename__: str = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    num_tokens: int
    status: Optional[str] = Field(default="processing")
    status_message: Optional[str] = Field(default="Order created")
    last_updated: Optional[datetime] = Field(default=datetime.utcnow())
    created_at: Optional[datetime] = Field(default=datetime.utcnow())
