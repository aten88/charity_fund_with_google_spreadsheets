from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.models import User
from app.services.base import BaseService


class DonationService(BaseService):
    """ Класс-сервис для донатов. """

    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session),
            user: User = Depends(current_user),
            obj_type: str = "DONAT"
    ):
        self.session = session
        self.user = user
        self.obj_type = obj_type
