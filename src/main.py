import src.db_services as _services
from src.database import get_session
from src.redis import RedisResource, Queue

from src.models import OrderCreate
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlmodel import Session

app = FastAPI()

_services.create_database()

load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create-order", status_code=201)
async def create_order(
    order_info: OrderCreate,
    session: Session = Depends(get_session),
):
    order = await _services.create_order(order_info, session)

    survival_bag = {
        "order_id": order.id,
        "user_id": order.user_id,
        "num_tokens": order.num_tokens,
    }

    RedisResource.push_to_queue(Queue.payment_queue, survival_bag)


@app.get("/get-orders")
async def get_orders(user_id: int, session: Session = Depends(get_session)):
    orders = await _services.get_orders(user_id, session)
    return orders
