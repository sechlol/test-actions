from pydantic import BaseModel


class Event(BaseModel):
    id: str
    name: str
    description: str | None = None
