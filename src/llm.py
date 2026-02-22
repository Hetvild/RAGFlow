from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

from core.config import settings


def get_llm():
    """
    Фабрика для создания LLM.
    Вынесена в отдельную функцию для удобства тестирования и замены провайдера.
    """
    return ChatOpenAI(
        model=settings.LLM_MODEL_NAME,
        api_key=settings.LLM_API_KEY,
        base_url=settings.LLM_BASE_URL,
        temperature=0.7,
        max_retries=2,
        timeout=30,
    )


# Пример использования
llm = get_llm()
messages = [HumanMessage(content="Расскажи кратко, что такое LangChain?")]
response = llm.invoke(messages)

print(response.content)
