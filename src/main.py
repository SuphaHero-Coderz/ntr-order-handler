import src.db_services as _services
from src.database import get_session
from src.redis import RedisResource, Queue
from src.exceptions import ForcedFailureError

from src.models import OrderCreate
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlmodel import Session
from fastapi_utils.tasks import repeat_every
from opentelemetry.trace.propagation.tracecontext import TraceContextTextMapPropagator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

provider = TracerProvider()
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)

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
    try:
        with tracer.start_as_current_span("create order"):
            order = await _services.create_order(order_info, session)
            # add trace context into the survival bag so receiver service can create span
            carrier = {}
            TraceContextTextMapPropagator().inject(carrier)

            if order_info.order_fail:
                raise ForcedFailureError

            survival_bag = {
                **order_info.__dict__,
                "task": "do_work",
                "order_id": order.id,
                "traceparent": carrier["traceparent"],
            }

            RedisResource.push_to_queue(Queue.payment_queue, survival_bag)
    except Exception as e:
        await update_order_status(
            order_id=order.id,
            status="failed",
            status_message=e.message,
            session=session,
        )


@app.get("/get-orders")
async def get_orders(user_id: int, session: Session = Depends(get_session)):
    orders = await _services.get_orders(user_id, session)
    return orders


@app.get("/get-order")
async def get_order(order_id: int, session: Session = Depends(get_session)):
    order = await _services.get_order(order_id, session)
    return order


@app.get("/get-all-orders")
async def get_all_orders(session: Session = Depends(get_session)):
    orders = await _services.get_all_orders(session)
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
