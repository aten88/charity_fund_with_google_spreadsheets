from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """ Схема для получения объекта User. """
    pass


class UserCreate(schemas.BaseUserCreate):
    """ Схема для создания объекта User. """
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """ Схема для обновления объекта User. """
    pass
