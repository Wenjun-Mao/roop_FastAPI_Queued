import requests
import time

from celery import Celery
from celery.utils.log import get_task_logger
# from api_data_sender import celery_send_return_data_to_api as _send_return_data_to_api

celery_logger = get_task_logger(__name__)

celery_app = Celery(
    "my_celery_app", 
    broker="pyamqp://guest@localhost//",
    backend='rpc://'
)

sync_max_retries = 3
destination_url = "http://localhost:8000/destination"

def _celery_send_return_data_to_api(id_value, download_url):
    data = {
        "url": download_url,
        "id": id_value,
    }
    celery_logger.info(f"Sending data to destination API: {data}")
    
    for attempt in range(sync_max_retries):
        try:
            response_E = requests.post(destination_url, json=data, timeout=20)
            celery_logger.info(f"Response from destination API: {response_E.status_code} {response_E.json()} id: {id_value}")
            response_E.raise_for_status()
            break
        except requests.RequestException as e:
            celery_logger.error(f"Failed request to destination API on attempt {attempt+1}: {e}")
            if attempt < sync_max_retries - 1:
                time.sleep(5) 
            else:
                celery_logger.error("All attempts failed.")
                raise


@celery_app.task(bind=True)
def celery_send_return_data_to_api(self, id_value, download_url):
    print("Task started")
    celery_logger.info(f"Task started: send_return_data_to_api({id_value}, {download_url})")
    try:
        # _celery_send_return_data_to_api(id_value, download_url)
        print(f'celery_send_return_data_to_api({id_value}, {download_url})')
        celery_logger.info(f"Task succeeded: send_return_data_to_api({id_value}, {download_url})")
    except Exception as e:
        celery_logger.error(f"Task failed: send_return_data_to_api({id_value}, {download_url}), error: {e}")
        raise