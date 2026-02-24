from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Role(Enum):
    admin = "admin"
    client = "client"
    master = "master"


class User(Base):
    """
    Модель таблицы Users для хранения данных о пользователях
    """

    username: Mapped[str] = mapped_column(String(50), unique=True)
    first_name: Mapped[str] = mapped_column(String(100), unique=False, nullable=True)
    last_name: Mapped[str] = mapped_column(String(150), unique=False, nullable=True)
    phone: Mapped[str] = mapped_column(String(15), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    telegram_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=True, comment="Messenger Telegram ID", index=True
    )
    max_id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=True, comment="Messenger MAX ID", index=True
    )
    role: Mapped[Role] = mapped_column(
        SQLEnum(Role), unique=False, default=Role.client, nullable=True
    )
    is_active: Mapped[bool] = mapped_column(unique=False, nullable=True, default=False)
