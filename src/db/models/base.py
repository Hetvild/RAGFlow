from datetime import datetime

from sqlalchemy import Integer, func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """
    Базовый класс для всех моделей в базе данных.

    Данный класс служит основой для создания всех ORM-моделей с использованием SQLAlchemy.
    Включает в себя общие поля: идентификатор, даты создания и обновления записи.
    Автоматически формирует имя таблицы на основе имени класса.

    Атрибуты:
        __abstract__ (bool): Указывает, что класс является абстрактным и не должен
                             создавать таблицу в базе данных.
        id (Mapped[int]): Уникальный идентификатор записи, первичный ключ, автоинкремент.
        created_at (Mapped[datetime]): Дата и время создания записи.
                                       Устанавливается автоматически при вставке.
        updated_at (Mapped[datetime]): Дата и время последнего обновления записи.
                                       Обновляется автоматически при изменении строки.

    Методы:
        __tablename__ (declared_attr): Генерирует имя таблицы как нижний регистр имени класса
                                       с добавлением суффикса 's' (например, User -> users).
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Автоматически генерирует имя таблицы для модели.

        Формат: имя класса в нижнем регистре + 's'.

        Возвращает:
            str: Имя таблицы в базе данных.
        """
        return cls.__name__.lower() + "s"
