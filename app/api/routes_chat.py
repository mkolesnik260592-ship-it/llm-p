from fastapi import APIRouter, Depends, Query
from app.schemas.chat import ChatRequest, ChatResponse
from app.api.deps import get_chat_usecase, get_current_user_id
from app.usecases.chat import ChatUsecase

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def ask(
    request: ChatRequest,
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUsecase = Depends(get_chat_usecase)
    ):
    """Отправляет prompt к LLM и возвращает ответ."""

    answer = await usecase.ask(user_id, request.prompt, request.system, request.max_history, request.temperature)
    return ChatResponse(answer=answer)

@router.get("/history")
async def get_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUsecase = Depends(get_chat_usecase),
    limit: int = Query(10, ge=1, le=100)
    ):
    """Возвращает историю диалога пользователя."""

    messages_list = await usecase.get_history(user_id, limit)
    return messages_list

@router.delete("/history")
async def delete_history(
    user_id: int = Depends(get_current_user_id),
    usecase: ChatUsecase = Depends(get_chat_usecase)
    ):
    """Очищает всю историю диалога пользователя."""

    await usecase.clear_history(user_id)
    return {"message": "History cleared"}
