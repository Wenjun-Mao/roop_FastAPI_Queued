# dramatiq_callback_worker.py

import dramatiq
import requests
from dramatiq.brokers.rabbitmq import RabbitmqBroker
import json

from api_app_config import RabbitmqBrokerAddress, callback_url
from api_logger_config import get_logger

logger = get_logger(__name__)

broker = RabbitmqBroker(url=f"amqp://{RabbitmqBrokerAddress}")
dramatiq.set_broker(broker)


def _dramatiq_send_return_data_to_api(id_value: str, download_url: str) -> None:
    data = {
        "url": download_url,
        "id": id_value,
    }
    logger.info(f"Sending data to callback API: {data}")

    response = requests.post(callback_url, json=data, timeout=5)

    try:
        response_json = response.json()
        logger.info(
            f"Response from callback API: {response.status_code} {response_json} id: {id_value}"
        )
    except json.JSONDecodeError:
        logger.info(
            f"Non-JSON response from callback API: {response.status_code} {response.text} id: {id_value}"
        )

    response.raise_for_status()


@dramatiq.actor(queue_name="callback_queue", max_retries=15, min_backoff=5000, time_limit=10000)
def dramatiq_send_return_data_to_api(id_value, download_url):
    logger.info(f"Task started: send_return_data_to_api({id_value}, {download_url})")
    try:
        _dramatiq_send_return_data_to_api(id_value, download_url)
        logger.info(
            f"Task succeeded: send_return_data_to_api({id_value}, {download_url})"
        )
    except Exception as e:
        logger.error(
            f"Task failed: send_return_data_to_api({id_value}, {download_url}), error: {e}"
        )
        raise
