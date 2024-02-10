from datetime import datetime

from sqlalchemy import (
    Column, String,
    Text, Integer,
    Boolean, DateTime
)

from app.core.constants import INVESTED_AMOUNT_START, MAX_LEN_FIELD
from app.core.db import Base


class CharityProject(Base):
    """ Модель проектов. """

    __tablename__ = 'charityproject'

    name = Column(String(MAX_LEN_FIELD), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=INVESTED_AMOUNT_START)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
