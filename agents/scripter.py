from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_script(summary: str, format: str = "short YouTube-style video") -> str:
    prompt = (
        f"Turn the following polished summary into a {format} script. Include a strong hook, "
        "narration, and any scene suggestions if relevant:\n\n" + summary
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
