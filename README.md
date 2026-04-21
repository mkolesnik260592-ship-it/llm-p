# LLM-P — защищённый API для работы с LLM

FastAPI приложение с JWT аутентификацией, хранением данных в SQLite и интеграцией с OpenRouter.

## Технологии

- FastAPI
- JWT (python-jose)
- SQLAlchemy (async, SQLite)
- OpenRouter API
- uv — управление зависимостями

## Установка и запуск

1. **Клонировать репозиторий**
git clone https://github.com/mkolesnik260592-ship-it/llm-p
cd llm-p

2. **Установить uv**
pip install uv

3. **Создать виртуальное окружение и активировать**
uv venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

4. **Установить зависимости**
uv pip install -r requirements.txt

5. **Создать файл .env**
JWT_SECRET=your_secret_key
OPENROUTER_API_KEY=your_api_key

6. **Запустить сервер**
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

7. **Открыть документацию**
http://localhost:8000/docs

### Эндпоинты

Метод	Путь	Описание	Авторизация
POST	/auth/register	Регистрация	Нет
POST	/auth/login	Получение JWT	Нет
GET	/auth/me	Профиль	Да
POST	/chat/	Запрос к LLM	Да
GET	/chat/history	История диалога	Да
DELETE	/chat/history	Очистка истории	Да
GET	/health	Проверка здоровья	Нет

#### Скриншоты
Регистрация
https://drive.google.com/file/d/1SURfqUtQeA3CqFXRNJN20arL65IAP2qB/view?usp=drive_link

Логин и получение токена
https://drive.google.com/file/d/10x32NKp6P4zyxgRyZzyG5RgUpWMoqcBI/view?usp=drive_link

Авторизация в Swagger
https://drive.google.com/file/d/1tnX_Nux2IQ-C_S5ahoCgFD2R0Z1Pc-Z4/view?usp=drive_link

Запрос к LLM
https://drive.google.com/file/d/1JffRQ1OrZ5Ffu5HjXWAYRIp_1PJ48mhP/view?usp=drive_link

История диалога
https://drive.google.com/file/d/1e-ZKozKIMcu58JKhQtWobwMGEXRnrJOz/view?usp=drive_link

Удаление истории
https://drive.google.com/file/d/11L6795f7OKBgLMWY9O6L9QaZbcSvvM9t/view?usp=drive_link

##### Проверка кода

ruff check

*Автор*
Студент: Колесник Матвей Анатольевич
Группа: M25-555
Email: mkolesnik260592@gmail.com
