import httpx
from app.core.config import settings
from app.core.errors import ExternalServiceError


class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.openrouter_base_url
        self.api_key = settings.openrouter_api_key
        self.default_model = settings.openrouter_model
        self.headers = {
                "Authorization": f"Bearer {self.api_key}",
                "HTTP-Referer": f"{settings.openrouter_site_url}",
                "X-Title": f"{settings.openrouter_app_name}"
        }

    async def chat_completion(self, messages: list, model: str = None, temperature: float = 0.7) -> str:
        """Отправляет запрос к LLM. Возвращает текст ответа модели."""

        target_model = model or self.default_model
        payload = {
            "model": target_model,
            "messages": messages,
            "temperature": temperature
        }

        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/chat/completions"
                response = await client.post(url, json=payload, headers=self.headers)
                if response.status_code == 200:
                    result = response.json()
                else:
                    raise ExternalServiceError(f"API returned error: {response.status_code} - {response.text}")
                return result["choices"][0]["message"]["content"]

            except httpx.HTTPStatusError as exc:
                raise ExternalServiceError(f"API status error: {exc.response.status_code} - {exc.response.text}")

            except httpx.RequestError as exc:
                raise ExternalServiceError(f"Network error: {str(exc)}")

            except (KeyError, IndexError) as exc:
                raise ExternalServiceError(f"Parsing error: missing key or index {str(exc)}")
