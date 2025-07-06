from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

# agents/scene_planner.py
from agent_base import RoleAgent

scene_planner = RoleAgent(
    name="Scene Planner",
    goal="Break the summary into a list of short, atomic visual scene blocks for a video script.",
    model=model,
    memory_file="memory/scene_planner.json"
)