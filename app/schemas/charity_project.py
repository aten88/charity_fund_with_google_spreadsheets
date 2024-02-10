from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra

from app.core.constants import MAX_LEN_FIELD, MIN_LEN_FIELD


class CharityProjectBase(BaseModel):
    """ Основа для схем проекта. """
    name: str = Field(
        None,
        min_length=MIN_LEN_FIELD,
        max_length=MAX_LEN_FIELD
    )
    description: str = Field(
        None,
        max_length=MAX_LEN_FIELD
    )
    full_amount: PositiveInt


class CharityProjectCreate(CharityProjectBase):
    """ Схема для создания обьекта CharityProject. """
    name: str = Field(max_length=MAX_LEN_FIELD)
    description: str


class CharityProjectDB(CharityProjectBase):
    """ Схема получения обьектов CharityProject из БД. """
    close_date: Optional[datetime]
    create_date: datetime
    description: str
    full_amount: PositiveInt
    fully_invested: bool
    id: int
    invested_amount: int
    name: str = Field(max_length=MAX_LEN_FIELD)

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    """ Схема для обновления обьекта CharityProject. """
    full_amount: Optional[PositiveInt]
    description: str = Field(None, min_length=MIN_LEN_FIELD)

    class Config:
        extra = Extra.forbid
