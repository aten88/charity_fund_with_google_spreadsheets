from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

from app.core.constants import MIN_LEN_FIELD


class DonationBase(BaseModel):
    """ Основа для схем пожертвования. """
    full_amount: PositiveInt
    comment: str = Field(None, min_length=MIN_LEN_FIELD)


class DonationCreate(DonationBase):
    """ Схема для создания пожертвования. """
    comment: Optional[str]


class DonationDB(DonationBase):
    """ Схема для получения пожертвования из БД. """
    comment: Optional[str]
    id: int
    create_date: datetime
    user_id: Optional[int]
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationUserDB(DonationBase):
    """ Схема для получения пожертвования юзера из БД. """
    comment: Optional[str]
    id: int
    create_date: datetime

    class Config:
        orm_mode = True
