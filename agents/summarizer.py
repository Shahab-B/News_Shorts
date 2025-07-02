# agents/summarizer.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def summarize_article(text: str, style: str = "short") -> str:
    prompt = f"Summarize the following news article in a {style} and informative tone:\n\n{text}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
