# Purpose: Receive a file from a client and save it to a local directory.

import os

from typing import Optional
from urllib.parse import unquote

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse

from api_logger_config import get_logger
from api_app_config import media_path
from api_util_content_manager import save_incoming_file


logger = get_logger(__name__)
app = FastAPI()


@app.post("/")
async def receive_user_request(
    content_type: str = Form(...),
    file: Optional[UploadFile] = File(None),
    url: Optional[str] = Form(None),
    id: str = Form(...),
):
    url = unquote(url) if url else None
    logger.info(
        "content_type: %s, file: %s, url: %s",
        content_type,
        file,
        url,
    )

    # if content_type == "picture", create file name as id.jpg
    # and path will be f"{media_path}/api_video_templates"
    # if content_type == "video", create file name as id+"l".mp4
    # and path will be f"{media_path}/api_pic_templates"

    if content_type == "picture":
        file_name = id + ".jpg"
        file_dir = f"{media_path}/api_video_templates"
    elif content_type == "video":
        file_name = id + "l.mp4"
        file_dir = f"{media_path}/api_pic_templates"

    file_path = os.path.join(file_dir, file_name)

    # save the file
    try:
        await save_incoming_file(file, url, file_path)
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        return JSONResponse(
            status_code=500,
            content={"message": f"Error occurred: {e}"},
        )

    return JSONResponse(
        status_code=200,
        content={"message": f"{file_name} saved successfully."},
    )
