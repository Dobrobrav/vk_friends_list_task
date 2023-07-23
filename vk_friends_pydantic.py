from typing import Literal

from pydantic import BaseModel


class ResponseWrapper(BaseModel):
    response: 'Response'


class Response(BaseModel):
    count: int
    items: list['FriendData']


class FriendData(BaseModel):
    first_name: str | None
    last_name: str | None
    country: 'Country | None' = None
    city: 'City | None' = None
    bdate: str | None = None
    sex: Literal[1, 2] | None = None


class City(BaseModel):
    id: int
    title: str


class Country(BaseModel):
    id: int
    title: str
