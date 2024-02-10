from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation, User


class CRUDDonations(CRUDBase):

    async def get_donations_by_user(
            self,
            session: AsyncSession,
            user: User,
    ):
        """ Метод получения донатов юзера. """
        donations = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return donations.scalars().all()


donation_crud = CRUDDonations(Donation)
