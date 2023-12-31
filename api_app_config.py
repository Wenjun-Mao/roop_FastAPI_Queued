# api_app_config.py

import os

from dotenv import find_dotenv, load_dotenv

_ = load_dotenv(find_dotenv())
callback_url = os.getenv("CALLBACK_URL")
callback_max_retries = int(os.getenv("CALLBACK_MAX_RETRIES"))
download_max_retries = int(os.getenv("DOWNLOAD_MAX_RETRIES"))
media_path = os.getenv("MEDIA_PATH")
server_address = os.getenv("SERVER_ADDRESS")
script_path = os.getenv("SCRIPT_PATH")
DEBUG = os.getenv("DEBUG") == "True"  # This will be a boolean
sd_webui_host = os.getenv("SD_WEBUI_HOST")
sd_webui_port = int(os.getenv("SD_WEBUI_PORT"))
default_video_path = os.getenv("DEFAULT_VIDEO_PATH")
default_picture_path = os.getenv("DEFAULT_PICTURE_PATH")
log_folder = os.getenv("LOG_FOLDER")
RabbitmqBrokerAddress = os.getenv("RABBITMQ_BROKER_ADDRESS")
roop_dir = os.getenv("ROOP_DIR")
