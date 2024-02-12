from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models import User
from app.services.investment_service import investment_process
from app.schemas.donation import DonationCreate


class DonationService:
    """ Класс-сервис для донатов. """

    def __init__(
            self,
            session: AsyncSession = Depends(get_async_session),
            user: User = Depends(current_user)
    ):
        self.session = session
        self.user = user

    async def create_donation(self, donation: DonationCreate,):
        """ Метод создания доната. """
        new_donation = await donation_crud.create(
            donation, self.session, self.user
        )
        await investment_process(new_donation, CharityProject, self.session)

        return new_donation