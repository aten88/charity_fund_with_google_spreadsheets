from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user, current_superuser
from app.crud.donation import donation_crud
from app.models import User
from app.services.projects_donats_services import DonationService
from app.schemas.donation import (
    DonationCreate,
    DonationDB,
    DonationUserDB
)


router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
    response_model_exclude_defaults=True,
)
async def create_donation(
    donation: DonationCreate,
    donation_service: DonationService = Depends()
):
    """ Сделать пожертвование. """

    return await donation_service.create_donation(donation)


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """ Только для суперюзеров.

    Получает список всех пожертвований.
    """
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    response_model_exclude_none=True,
)
async def get_user_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """ Получить список моих пожертвований. """
    all_donations = await donation_crud.get_donations_by_user(session=session, user=user)
    return all_donations
