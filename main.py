import os
import logging as LOG
import json
import uuid
import redis
from dotenv import load_dotenv
from src.models import Order
import src.db_services as _services

load_dotenv()

REDIS_QUEUE_LOCATION = os.getenv("REDIS_QUEUE", "localhost")
ORDER_QUEUE_NAME = os.getenv("ORDER_QUEUE_NAME")

QUEUE_NAME = f"queue:{ORDER_QUEUE_NAME}"
INSTANCE_NAME = uuid.uuid4().hex

LOG.basicConfig(
    level=LOG.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


def watch_queue(redis_conn, queue_name, callback_func, timeout=30):
    """
    Listens to queue `queue_name` and passes messages to `callback_func`
    """
    active = True

    while active:
        # Fetch a json-encoded task using a blocking (left) pop
        packed = redis_conn.blpop([queue_name], timeout=timeout)

        if not packed:
            # if nothing is returned, poll a again
            continue

        _, packed_task = packed

        # If it's treated to a poison pill, quit the loop
        if packed_task == b"DIE":
            active = False
        else:
            task = None
            try:
                task = json.loads(packed_task)
            except Exception:
                LOG.exception("json.loads failed")
                data = {"status": -1, "message": "An error occurred"}
                redis_conn.publish(ORDER_QUEUE_NAME, json.dumps(data))
            if task:
                callback_func(task)
                data = {"status": 1, "message": "Successfully chunked video"}
                redis_conn.publish(ORDER_QUEUE_NAME, json.dumps(task))


def process_message(data):
    """
    Processes an incoming message from the work queue
    """
    order = Order(user_id=data["user_id"], num_tokens=data["num_tokens"])
    _services.create_order(order)


def main():
    LOG.info("Starting a worker...")
    LOG.info("Unique name: %s", INSTANCE_NAME)
    host, *port_info = REDIS_QUEUE_LOCATION.split(":")
    port = tuple()

    if port_info:
        port, *_ = port_info
        port = (int(port),)

    named_logging = LOG.getLogger(name=INSTANCE_NAME)
    named_logging.info("Trying to connect to %s [%s]", host, REDIS_QUEUE_LOCATION)
    redis_conn = redis.Redis(host=host, *port)
    named_logging.info("Listening to queue: %s", QUEUE_NAME)

    watch_queue(redis_conn, QUEUE_NAME, process_message)


if __name__ == "__main__":
    _services.create_database()
    main()