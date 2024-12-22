from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI()


def ask(system_prompt: str, user_input: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
            {"role": "user", "content": [{"type": "text", "text": user_input}]},
        ],
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        frequency_penalty=0.5,
        presence_penalty=0,
        response_format={"type": "text"},
    )

    return response.choices[0].message.content or "ERROR OCCURS.\n"
