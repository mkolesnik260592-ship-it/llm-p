from app.repositories.chat_messages import ChatMessagesRepository
from app.services.openrouter_client import OpenRouterClient
from app.db.models import ChatMessage
from typing import List


class ChatUsecase:
    def __init__(self, chat_repository: ChatMessagesRepository, openrouter_client: OpenRouterClient):
        self.chat_repository = chat_repository
        self.openrouter_client = openrouter_client


    async def ask(
            self, user_id: int,
            prompt: str,
            system: str = None,
            max_history: int = 10,
            temperature: float = 0.7) -> str:
        """Отправляет запрос к LLM, сохраняет вопрос и ответ в истории. Возвращает ответ модели."""

        messages = []
        if system:
            system_msg = {
                "role": "system",
                "content": system}
            messages.insert(0, system_msg)
        history = await self.chat_repository.get_history(user_id, max_history)
        for msg in history:
            messages.append({"role": msg.role, "content": msg.content})
        user_message = {
            "role": "user",
            "content": prompt}
        messages.append(user_message)

        await self.chat_repository.add_message(user_id=user_id, role="user", content=prompt)
        answer = await self.openrouter_client.chat_completion(messages, temperature=temperature)
        await self.chat_repository.add_message(user_id=user_id, role="assistant", content=answer)
        return answer

    async def get_history(self, user_id: int, limit: int = 10) -> List[ChatMessage]:
        """Возвращает последние limit сообщений пользователя."""

        return await self.chat_repository.get_history(user_id, limit)

    async def clear_history(self, user_id: int) -> None:
        """Удаляет всю историю сообщений пользователя."""

        await self.chat_repository.delete_history(user_id)
