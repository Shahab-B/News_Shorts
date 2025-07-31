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
    goal=(
        "You are a critic agent evaluating narration and scene descriptions for clarity, emotional pacing, and viewer engagement. "
        "Provide specific, constructive feedback on what to improve and why. "
        "Highlight unclear visual references, pacing issues, or weak emotional beats. "
        "If previous critiques exist in memory, refer to them to maintain consistency in evaluation standards."
    ),
    model=model,
    memory_file="memory/critic.json"
)