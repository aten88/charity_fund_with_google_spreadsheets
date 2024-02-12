from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.constants import BOOLEAN_VARIABLE
from app.models import CharityProject, Donation


def closing_process(obj: Union[CharityProject, Donation]) -> Union[CharityProject, Donation]:
    """ Закрывает проект/донат публикует дату закрытия. """
    obj.fully_invested = True
    obj.close_date = datetime.now()
    return obj


def reinvestment_process(
    new_obj: Union[CharityProject, Donation],
    open_obj: Union[CharityProject, Donation],
):
    """Метод перераспределения сумм между Донатами/Проектами."""
    to_close_new_obj = new_obj.full_amount - new_obj.invested_amount
    to_close_open_obj = open_obj.full_amount - open_obj.invested_amount
    to_close = min(to_close_new_obj, to_close_open_obj)
    open_obj.invested_amount += to_close
    new_obj.invested_amount += to_close

    return new_obj, open_obj


async def investment_process(
    new_obj: Union[CharityProject, Donation],
    model: Union[CharityProject, Donation],
    session: AsyncSession,
) -> None:
    """ Метод инвестирования Донатов/Проектов. """
    all_open_objs = await session.execute(
        select(model).where(model.fully_invested == BOOLEAN_VARIABLE)
    )
    all_open_objs = all_open_objs.scalars().all()
    for open_obj in all_open_objs:
        new_obj, open_obj = reinvestment_process(new_obj, open_obj)
        if open_obj.invested_amount == open_obj.full_amount:
            open_obj = closing_process(open_obj)
        session.add(open_obj)
        if new_obj.invested_amount == new_obj.full_amount:
            new_obj = closing_process(new_obj)
            break
    session.add(new_obj)
    await session.commit()
    await session.refresh(new_obj)
