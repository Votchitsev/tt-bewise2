from pydantic import BaseModel

class AuthQuery(BaseModel):
    name: str
