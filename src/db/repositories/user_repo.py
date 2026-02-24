from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging import logger
from db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        """Получить пользователя по Telegram ID"""
        query = select(User).where(User.telegram_id == telegram_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create_user(
        self, username: str, email: str = None, telegram_id: int = None
    ) -> User:
        """Создать нового пользователя"""
        new_user = User(username=username, email=email, telegram_id=telegram_id)
        self.session.add(new_user)
        try:
            await self.session.commit()
            await self.session.refresh(new_user)
            logger.debug("Пользователь создан с ID: {}", new_user.id)
            return new_user
        except Exception as e:
            await self.session.rollback()
            logger.error("Ошибка при создании: {}", e)
            raise e

    async def get_or_create_user(
        self, username: str, email: str = None, telegram_id: int = None
    ) -> User:
        """Получить пользователя, а если нет - создать"""
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            return user

        # Если не найден, создаем
        return await self.create_user(
            username=username, email=email, telegram_id=telegram_id
        )
