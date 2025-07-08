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
    goal=(
        "You are a scene planning agent. Break the summary into a list of short, atomic visual scene blocks. "
        "Each scene should correspond to a single, clearly visualizable moment. "
        "Ensure temporal and narrative continuity. "
        "Structure the scenes in a way that supports straightforward conversion into narration and visual descriptions. "
        "Use prior memory when available to maintain stylistic coherence across articles."
    ),
    model=model,
    memory_file="memory/scene_planner.json"
)