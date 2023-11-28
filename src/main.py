import src.db_services as _services
from src.database import get_session
from src.redis import RedisResource, Queue

from src.models import OrderCreate
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlmodel import Session
from fastapi_utils.tasks import repeat_every

app = FastAPI()

_services.create_database()

load_dotenv()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@repeat_every(seconds=60)
async def update_expired_orders() -> None:
    await _services.update_expired_orders()


@app.on_event("startup")
async def startup() -> None:
    await update_expired_orders()


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
        "user_credits": order_info.user_credits,
    }

    RedisResource.push_to_queue(Queue.payment_queue, survival_bag)


@app.get("/get-orders")
async def get_orders(user_id: int, session: Session = Depends(get_session)):
    orders = await _services.get_orders(user_id, session)
    return orders


@app.put("/update-order-status")
async def update_order_status(
    order_id: int,
    status: str,
    status_message: str,
    session: Session = Depends(get_session),
):
    await _services.update_order_status(
        order_id=order_id, status=status, status_message=status_message, session=session
    )
