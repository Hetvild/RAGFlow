import hashlib

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger


def split_text(text: str) -> list[Document]:
    """
    Функция разделяет текст на чанки

    Args:
        text (str): текст для разделения

    Returns:
        list(str): список чанков
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )

    documents = [Document(page_content=text)]
    split_docs = text_splitter.split_documents(documents)

    return split_docs


def generate_chunk_id(text: str, index: int) -> str:
    """
    Генерируем уникальный id на основе содержания текста

    Args:
        text (str): Текст
        index (int): Индекс чанка
    """

    content = f"{text}_{index}"

    hash_id: str = hashlib.md5(content.encode("utf-8")).hexdigest()
    logger.info(f"Generated chunk id: {hash_id}")

    return hash_id
