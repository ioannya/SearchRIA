import os
import httpx
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL")

SYSTEM_PROMPT = """Ты — помощник, который отвечает на вопросы пользователя ТОЛЬКО на основе документов, приложенных ниже.

Правила:
1. Отвечай только на основе предоставленных документов.
2. Если документы не содержат ответа на вопрос — прямо скажи об этом, не придумывай ответ.
3. В конце ответа укажи, на какие документы (по номеру) ты опирался.
4. Отвечай кратко и по существу, на русском языке."""


def get_client():
    api_key = os.getenv("LLM_API_KEY")
    base_url = os.getenv("LLM_BASE_URL")
    if not api_key:
        raise RuntimeError(
            "LLM_API_KEY не задан. Проверь файл .env в корне проекта."
        )
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        http_client=httpx.Client(proxy="socks5://127.0.0.1:10808")
    )


def build_context(posts):
    parts = []
    for i, post in enumerate(posts, start=1):
        parts.append(f"[Документ {i}] {post['text']}\nСсылка: {post['url']}")
    return "\n\n".join(parts)


def summarize(query, posts):
    if not posts:
        return "По вашему запросу ничего не найдено в базе документов."

    client = get_client()
    context = build_context(posts)

    user_message = f"""Вопрос пользователя: {query}

Документы:
{context}"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
        max_tokens=500
    )

    return response.choices[0].message.content