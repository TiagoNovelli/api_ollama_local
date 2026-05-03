from openai import OpenAI

from config import settings


client = OpenAI(
    api_key=settings.openai_api_key,
    base_url=settings.openai_base_url,
)

response = client.chat.completions.create(
    model=settings.default_model,
    messages=[{"role": "user", "content": "Diga oi em uma frase"}],
)

print(response.choices[0].message.content)
