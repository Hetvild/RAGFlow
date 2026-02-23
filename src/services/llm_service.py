from typing import AsyncGenerator, Optional

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from core.config import settings


class LLMService:
    """
    Универсальный LLM-сервис через OpenAI-compatible API.
    """

    def __init__(
        self,
        base_url=settings.LLM_BASE_URL,
        api_key=settings.LLM_API_KEY,
        model=settings.LLM_MODEL_NAME,
        temperature=settings.LLM_TEMPERATURE,
        max_tokens: Optional[int] = None,
    ):

        self._llm = ChatOpenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            temperature=temperature,
            max_tokens=max_tokens,
            streaming=True,
            max_retries=2,
            timeout=30,
        )

    async def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[str] = None,
    ) -> str:
        """Полный ответ (не стрим)"""
        messages = self._build_messages(system_prompt, user_message, context)
        response = await self._llm.ainvoke(messages)
        return response.content

    async def generate_response_stream(
        self,
        system_prompt: str,
        user_message: str,
        context: Optional[str] = None,
    ) -> AsyncGenerator[str, None]:
        """Стриминг токенов для фронтенда"""
        messages = self._build_messages(system_prompt, user_message, context)
        async for chunk in self._llm.astream(messages):
            if chunk.content:
                yield chunk.content

    @staticmethod
    def _build_messages(
        # self,
        system_prompt: str,
        user_message: str,
        context: Optional[str] = None,
    ) -> list:
        """Формирует промпт с контекстом для RAG"""
        if context:
            system_prompt += (
                f"\n\nКонтекст из базы знаний:\n<context>\n{context}\n</context>"
            )

        return [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]


llm_service = LLMService()
