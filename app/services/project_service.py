from http import HTTPStatus

from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.crud.charity_project import project_crud
from app.models.charity_project import CharityProject
from app.services.validators import (
    check_name, check_charity_project_exists,
    check_fully_invested, check_fully_and_invested_amounts,
)
from app.schemas.charity_project import CharityProjectUpdate
from app.services.base import BaseService


async def validate_full_amount(update_data, db_obj):
    """ Проверяет поле full_amount. """
    if 'full_amount' in update_data and update_data['full_amount'] < db_obj.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Сумма проекта не может быть меньше инвестированной суммы!'
        )


class CharityProjectService(BaseService):
    """ Класс-сервис для проектов. """

    def __init__(self, session: AsyncSession = Depends(get_async_session), obj_type: str = "PROJECT"):
        self.session = session
        self.obj_type = obj_type

    async def update_charity_project(self, project_id: int, obj_in: CharityProjectUpdate,):
        """ Метод обновления проекта. """

        await check_charity_project_exists(project_id, self.session)
        await check_fully_invested(project_id, self.session)

        if obj_in.name is not None:
            await check_name(obj_in.name, self.session)

        charity_project = await project_crud.get(project_id, self.session)

        await validate_full_amount(obj_in.dict(exclude_unset=True), charity_project)

        return await project_crud.update(charity_project, obj_in, self.session)

    async def delete_charity_project(self, project_id: int,):
        """ Метод удаления проекта. """

        await check_fully_and_invested_amounts(project_id, self.session)
        await check_charity_project_exists(project_id, self.session)

        charity_project = await project_crud.get(project_id, self.session)

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
