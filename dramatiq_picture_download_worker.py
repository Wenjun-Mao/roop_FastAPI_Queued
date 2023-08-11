# dramatiq_picture_download_worker.py

import dramatiq
import requests
import time
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from typing import Optional
from fastapi import UploadFile

from api_app_config import RabbitmqBrokerAddress, download_max_retries
from api_logger_config import get_logger
from dramatiq_media_process_worker import dramatiq_media_process

logger = get_logger(__name__)

broker = RabbitmqBroker(url=f"amqp://{RabbitmqBrokerAddress}")
dramatiq.set_broker(broker)


def download_from_url_with_retry(url: str, timeout: int = 5, max_attempts: int = 3):
    max_attempts = download_max_retries
    start_time = time.time()
    attempts = 0
    while attempts < max_attempts:
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()  # Raise exception if status code is not 200
            logger.info(
                "Picture received in %s seconds with %s attempt(s).",
                round(time.time() - start_time, 2),
                attempts + 1,
            )
            return response
        except (requests.Timeout, requests.HTTPError):
            attempts += 1
            time.sleep(2)  # Wait for 2 seconds before next attempt
    raise requests.Timeout(f"Failed to retrieve {url} after {max_attempts} attempts")


def save_incoming_file(
    file: Optional[UploadFile], url: Optional[str], incoming_file_path: str
):
    if file:
        with open(incoming_file_path, "wb") as buffer:
            buffer.write(file.file.read())
    elif url:
        response = download_from_url_with_retry(url)
        with open(incoming_file_path, "wb") as buffer:
            buffer.write(response.content)


@dramatiq.actor(queue_name="picture_download_queue", max_retries=15, min_backoff=5000, time_limit=30000)
def dramatiq_picture_download(
    file,
    url,
    id_value,
    content_type,
    content_name,
    face_restore,
    incoming_file_path,
):
    logger.info(f"Task started: picture_download({file}, {url}, {id_value})")
    save_incoming_file(file, url, incoming_file_path)
    logger.info(f"Task finished: picture_download({file}, {url}, {id_value})")
    dramatiq_media_process.send(
        content_type,
        incoming_file_path,
        content_name,
        face_restore,
        id_value,
    )
