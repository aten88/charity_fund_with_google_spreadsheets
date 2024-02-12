from http import HTTPStatus

from fastapi import HTTPException

from app.crud.charity_project import project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.models.donation import Donation
from app.services.investment_service import investment_process
from app.services.validators import check_name


async def check_description(project_description: str):
    """ Валидатор для проверки описания. """
    if not project_description:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Описание проекта не может быть пустым!'
        )


class BaseService:
    """ Базовый сервисный класс. """

    async def create(self, obj_in):
        """ Универсальный метод создания. """

        if self.obj_type == 'DONAT':
            new_donation = await donation_crud.create(
                obj_in, self.session, self.user
            )
            return await investment_process(new_donation, CharityProject, self.session)
        if self.obj_type == 'PROJECT':

            await check_name(obj_in.name, self.session)
            await check_description(obj_in.description)

            new_project = await project_crud.create(obj_in, self.session)

            return await investment_process(new_project, Donation, self.session)
        else:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Неизвестный тип операции!'
            )
