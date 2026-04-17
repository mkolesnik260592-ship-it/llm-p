class AppError(Exception):
    """Базовое исключение приложения"""
    pass


class ConflictError(AppError):
    """Конфликт: ресурс уже существует"""
    pass


class UnauthorizedError(AppError):
    """Не авторизован: неверный email/пароль или отсутствует токен"""
    pass


class ForbiddenError(AppError):
    """Доступ запрещён: недостаточно прав"""
    pass


class NotFoundError(AppError):
    """Ресурс не найден"""
    pass


class ExternalServiceError(AppError):
    """Ошибка внешнего сервиса"""
    pass
