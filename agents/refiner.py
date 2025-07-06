# agents/refiner.py
from agent_base import RoleAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

refiner = RoleAgent(
    name="Refiner",
    goal="Improve the original script using the critic's feedback. Do not deviate from the story.",
    model=model,
    memory_file="memory/refiner.json"
)