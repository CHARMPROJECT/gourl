from pydantic import BaseModel, Field, HttpUrl

class CreateUrlRequestSchema(BaseModel):
    url: HttpUrl

class CreateUrlResponseSchema(BaseModel):
    path: str
