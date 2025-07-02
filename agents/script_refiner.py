from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def polish_script(script: str, goal: str = "maximize engagement and emotional impact") -> str:
    prompt = (
        f"Polish the following video script to {goal}. Improve pacing, strengthen the hook, and make sure it keeps the viewer interested throughout:\n\n{script}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
