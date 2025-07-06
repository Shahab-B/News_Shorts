# agents/critic.py
from agent_base import RoleAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

critic = RoleAgent(
    name="Critic",
    goal="Review the narration and scenes for clarity, pacing, and emotional engagement. Suggest specific improvements.",
    model=model,
    memory_file="memory/critic.json"
)