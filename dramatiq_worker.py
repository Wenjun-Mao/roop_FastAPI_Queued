import requests
import time
import dramatiq
from api_app_config import destination_url, sync_max_retries
from api_logger_config import get_logger

logger = get_logger(__name__)


def _dramatiq_send_return_data_to_api(id_value, download_url):
    data = {
        "url": download_url,
        "id": id_value,
    }
    logger.info(f"Sending data to destination API: {data}")
    
    for attempt in range(sync_max_retries):
        try:
            response_E = requests.post(destination_url, json=data, timeout=5)
            logger.info(f"Response from destination API: {response_E.status_code} {response_E.json()} id: {id_value}")
            response_E.raise_for_status()
            break
        except requests.RequestException as e:
            logger.error(f"Failed request to destination API on attempt {attempt+1}: {e}")
            if attempt < sync_max_retries - 1:
                time.sleep(5) 
            else:
                logger.error("All attempts failed.")
                raise


@dramatiq.actor
def dramatiq_send_return_data_to_api(id_value, download_url):
    print("Task started")
    logger.info(f"Task started: send_return_data_to_api({id_value}, {download_url})")
    try:
        _dramatiq_send_return_data_to_api(id_value, download_url)
        print(f'dramatiq_send_return_data_to_api({id_value}, {download_url})')
        logger.info(f"Task succeeded: send_return_data_to_api({id_value}, {download_url})")
    except Exception as e:
        logger.error(f"Task failed: send_return_data_to_api({id_value}, {download_url}), error: {e}")
        raise