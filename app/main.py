import os
import uuid
from fastapi import FastAPI, HTTPException, Request, status, UploadFile, Form, File
from fastapi.responses import JSONResponse, FileResponse
from typing import Annotated
from pydantic.error_wrappers import ValidationError
from .interface import AuthQuery
from asyncpg.exceptions import UniqueViolationError
from .FileStorage import FileStorage
from .db import database, User


app = FastAPI()

storage = FileStorage(os.path.abspath('./app/storage'))


@app.get('/')
def root():
    return None


@app.post('/auth')
async def auth(query: AuthQuery):
    response = await User.objects.create(
        name=query.name
    )

    return {
        'id': response.id,
        'uuid': response.uuid,
    }


@app.post('/upload')
async def upload_file(
    file: Annotated[UploadFile, File()],
    user_id: Annotated[int, Form()],
    user_uuid: Annotated[str, Form()],
):
    if file.content_type != "audio/wav":
        raise HTTPException(    
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Not wav file.'
        )

    user = await User.objects.get_or_none(
        id=user_id,
        uuid=user_uuid,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid credentials'
        )

    collected_file = await storage.collect_file(uuid.uuid1(), file, user)

    if not collected_file:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="File doesn't collected",
        )

    return {
        'url': collected_file,
    }


@app.get('/record')
async def download_file(id: str, user_id: int):
    file = await storage.get_file(id, user_id)

    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='File not found.'
        )
    
    return FileResponse(
        path=file.path,
        filename='{record_id}.mp3'.format(record_id=id),
        media_type='multipart/form-data',
    )


@app.exception_handler(ValidationError)
async def validation_error_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': str(exc),
        }
    )


@app.exception_handler(UniqueViolationError)
async def unique_violation_error_handler(request: Request, exc: UniqueViolationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'error': str(exc),
        }
    )


@app.on_event('startup')
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event('shutdown')
async def shutdown():
    if database.is_connected:
        await database.disconnect()
