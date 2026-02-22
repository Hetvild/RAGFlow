import asyncio

from core.logging import logger
from services import EmbeddingsService
from utils.text_splitter import split_text


large_text = """Существует правило, нарушение которого приведет к неработоспособности поиска:
Модель для векторизации вопросов должна быть идентична модели для векторизации документов.
Если вы записывали документы в базу с помощью модели EmbeddingsGigaR, то и вопросы пользователей нужно превращать в векторы именно с помощью EmbeddingsGigaR.
Почему: Разные модели (или даже одна модель с разными параметрами) создают векторы в разных математических пространствах. Вектор от одной модели будет «непонятен» для векторов другой модели, и поиск выдаст случайные результаты."""


async def main():
    service = EmbeddingsService()
    # 1. Получить файл
    # 2. Определить расширение файла
    # 3. Разделить текст на чанки по правилам формата файлов
    # list_chunk_documents = split_text(large_text)
    list_chunk_documents = [doc.page_content for doc in split_text(large_text)]
    # 4. Получаем векторы для каждого чанка
    count = await service.index_documents(list_chunk_documents)

    logger.debug(f"Indexed documents: {count}")

    # Отправляем текст на обработку для получения его вектора
    # result = await get_embeddings(large_text)

    # Поиск (вызывается при каждом вопросе пользователя)
    context = await service.search_similar("Как настроить бота")
    logger.debug(f"Найденный контекст: {context}")


# Запуск асинхронной функции
asyncio.run(main())
