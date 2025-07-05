from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def polish_script(script: str, goal: str = "maximize engagement and tell the story chronologically as it occured focused on the key events.") -> str:
    prompt = (
        f"Polish the following video script to {goal}. Separate narration from the scene description. The description of each scene should be detailed enough for an ai video generator to have sufficient context of scenes before it. Improve pacing, strengthen the hook, and make sure it keeps the viewer interested throughout. Should still be the length of a youtube short.:\n\n{script}"
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
