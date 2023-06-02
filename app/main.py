from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic.error_wrappers import ValidationError
from .interface import AuthQuery
from asyncpg.exceptions import UniqueViolationError
from .db import database, User


app = FastAPI()


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
