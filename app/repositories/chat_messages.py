from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import ChatMessage
from typing import List


class ChatMessagesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str) -> ChatMessage:
        """Добавляет новое сообщение в историю. Возвращает созданное сообщение."""

        new_message = ChatMessage(
            user_id=user_id,
            role=role,
            content=content
        )
        self.session.add(new_message)
        await self.session.commit()
        await self.session.refresh(new_message)
        return new_message

    async def get_history(self, user_id: int, limit: int = 10) -> List[ChatMessage]:
        """Возвращает последние limit сообщений пользователя, отсортированные по времени."""

        history = (
            select(ChatMessage)
            .where(ChatMessage.user_id == user_id)
            .order_by(ChatMessage.created_at)
            .limit(limit))
        result = await self.session.execute(history)
        return result.scalars().all()

    async def delete_history(self, user_id: int) -> None:
        """Удаляет все сообщения пользователя из истории."""

        await self.session.execute(delete(ChatMessage).where(ChatMessage.user_id == user_id))
        await self.session.commit()
