# roop_FastAPI_Queued
When facing very high traffic, the roop_FastAPI server can be overloaded. To prevent this, roop_FastAPI_Queued added queueing to roop_FastAPI using RabbitMQ and Dramatiq.
roop_FastAPI is a web API wrapper for the "roop" project, designed to provide a user-friendly interface for interactions with the underlying roop system.
roop_FastAPI allow for sending a POST with headless args and retrieving output with GET once ready.
In order to improve the output capacity, this wrapper applies monkey patching on a few functions from the original roop project. This does not involve changing any code in the original roop repo.


## Description
This wrapper is developed with FastAPI and provides endpoints for both POST and GET requests. The POST endpoint allows users to send data which could include an image, a user identifier and other parameters.

The GET endpoint, on the other hand, allows users to download a processed video. Once the POST request is processed, a URL is provided where the user can download the resulting video. The GET endpoint can be used standalone or be coupled with Nginx for caching for improved performance.


## Features
- **Secure Data Handling:** All operations involving file processing and communication with external systems are protected by asyncio locks to ensure thread safety.
- **Error Handling:** The application provides meaningful HTTPException responses in case of errors during processing.
- **Background Tasks:** FastAPI's BackgroundTasks are used to send data to a destination API after returning the response.
- **Stable-diffusion-webui** can be called for further processing.
- **Environmental Variables:** Environmental variables are used to store sensitive data, such as server addresses and paths.


## Installation
To install this project, clone the repository and install the required dependencies of roop.

Then install FastAPI with the following command:
```
pip install fastapi[all] webuiapi
```

A .env file is needed to set the necessary environmental variables. .env-TEMPLATE is included in the repository as a template for the .env file. The following environmental variables are required:
- **MEDIA_PATH:** The path to the directory where the media files are stored.
- **SYNC_URL:** The URL of the archiving server.
- **SERVER_ADDRESS:** The address of the server where the finished files can be retrieved.
- **SCRIPT_PATH:** The path to the roop run script.


## Usage
Start both POST and GET service with uvicorn with desired settings.
Send a POST request to the / endpoint with the necessary parameters. If successful, the endpoint will return a download link that you can use to retrieve the processed video via the GET service.


## Endpoints
- **POST /**: Used to upload data for processing. Accepts parameters like an image, a user identifier, etc.
- **GET /download_video/{date}/{video_name}**: Used to download the processed video.
- **GET /download_pic/{date}/{pic_name}**: Used to download the processed picture.


## Contributing
Contributions to this project are welcome. Please open an issue first to discuss what you would like to change.
