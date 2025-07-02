from openai import OpenAI
from dotenv import load_dotenv
import os

# Load from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
organization = os.getenv("OPENAI_ORGANIZATION_ID")

client = OpenAI(api_key=api_key,organization=organization)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo", # gpt-4o gpt-4o-mini gpt-3.5-turbo dall-e-3 tts-*
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message)
