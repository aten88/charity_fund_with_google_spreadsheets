from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.donation import donation_crud
from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.models import User
from app.services.investments_service import investment_process
from app.services.validators import (
    check_name, check_description, check_charity_project_exists,
    check_fully_invested, validate_full_amount, check_fully_and_invested_amounts,
)
from app.schemas.charity_project import CharityProjectCreate, CharityProjectUpdate
from app.schemas.donation import DonationCreate


class CharityProjectService:
    """ Класс-сервис для проектов. """

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self.session = session

    async def create_charity_project(self, charity_project: CharityProjectCreate):
        """ Метод создания проекта. """

        await check_name(charity_project.name, self.session)
        await check_description(charity_project.description, self.session)

        new_project = await project_crud.create(charity_project, self.session)
        await investment_process(new_project, Donation, self.session)
        return new_project

    async def update_charity_project(self, project_id: int, obj_in: CharityProjectUpdate,):
        """ Метод обновления проекта. """

        await check_charity_project_exists(project_id, self.session)
        charity_project = await check_fully_invested(project_id, self.session)

        if obj_in.name is not None:
            await check_name(obj_in.name, self.session)

        await validate_full_amount(obj_in.dict(exclude_unset=True), charity_project, self.session)

        return await project_crud.update(charity_project, obj_in, self.session)

    async def delete_charity_project(self, project_id: int,):
        """ Метод удаления проекта. """

        await check_fully_and_invested_amounts(project_id, self.session)
        charity_project = await check_charity_project_exists(project_id, self.session)

        return await project_crud.remove(charity_project, self.session)

    async def get_projects_by_completion_rate(self):
        """ Метод сортировки проектов по времени закрытия. """
        projects = await self.session.execute(
            select(
                CharityProject.name,
                CharityProject.close_date,
                CharityProject.create_date,
                CharityProject.description).where(
                    CharityProject.fully_invested))
        results = []
        for project in projects:
            results.append(
                {
                    'name': project.name,
                    'collection_time': project.close_date - project.create_date,
                    'description': project.description
                }
            )
        return sorted(results, key=lambda x: x['collection_time'])


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
