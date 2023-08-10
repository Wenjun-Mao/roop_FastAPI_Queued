# api_post_dramatiq.py

import asyncio
import os

os.environ["OMP_NUM_THREADS"] = "1"

from typing import Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from api_logger_config import get_logger
from api_util_content_manager import create_incoming_file_path, validate_inputs
from dramatiq_picture_download_worker import dramatiq_picture_download

# from api_refactor_util import *

logger = get_logger(__name__)
app = FastAPI()
# lock = asyncio.Lock()


@app.exception_handler(ConnectionResetError)
async def handle_connection_reset_error(request, exc):
    logger.error(f"ConnectionResetError occurred: {exc}")
    return JSONResponse(
        status_code=500, content={"message": "---Unexpected connection error---"}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"An error occurred: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred. Please try again later."},
    )


@app.post("/")
async def receive_user_request(
    content_type: str = Form(...),
    content_name: str = Form(...),
    face_restore: Optional[int] = Form(0),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    id: str = Form(...),
):
    os.environ["NO_FACE"] = "0"

    url = unquote(url) if url else None
    logger.info(
        "content_name: %s, face_restore: %s, file: %s, url: %s",
        content_name,
        face_restore,
        file,
        url,
    )

    id_value = id
    logger.info(f"Received request for id: {id_value}")

    validate_inputs(content_type, content_name, file, url)
    incoming_file_path = create_incoming_file_path(file, url)
    dramatiq_picture_download.send(
        file,
        url,
        id_value,
        content_type,
        content_name,
        face_restore,
        incoming_file_path,
    )

    message = f"Request from ID: {id_value} received"
    logger.info(message)

    return {"message": message}
