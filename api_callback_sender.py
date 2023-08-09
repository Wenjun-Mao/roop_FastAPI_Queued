# api_callback_handler.py

import asyncio

import httpx

from api_app_config import callback_url, callback_max_retries
from api_logger_config import get_logger

logger = get_logger(__name__)


async def send_return_data_to_api(id_value, download_url):
    data = {
        "url": download_url,
        "id": id_value,
    }
    logger.info(f"Sending data to callback API: {data}")

    # Number of attempts to try sending the request
    max_attempts = callback_max_retries
    for attempt in range(max_attempts):
        try:
            async with httpx.AsyncClient() as client:
                response_E = await client.post(callback_url, json=data, timeout=5)
                logger.info(
                    f"Response from callback API: {response_E.status_code} {response_E.json()} id: {id_value}"
                )
                response_E.raise_for_status()
                break  # If successful, exit the loop
        except Exception as e:  # Catch other potential exceptions
            logger.warning(
                f"Attempt {attempt + 1} failed to send request to callback API: {e}"
            )

        if attempt < max_attempts - 1:  # If not the last attempt, sleep
            await asyncio.sleep(5)  # Sleep for 5 seconds between attempts

    else:  # If loop completes without a break, all attempts failed
        logger.error(
            f"Failed request to callback API after {max_attempts} attempts."
        )
        return False

    return True  # If successful
