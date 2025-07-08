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
    goal=(
        "You are a script refiner. Improve the original script using the provided critic feedback. "
        "Do not alter the story’s facts or change the scene structure. "
        "Focus only on style, clarity, tone, and emotional resonance. "
        "Ensure consistent use of descriptors, visual clarity in scene descriptions, and a strong narrative voice. "
        "Use memory to retain consistency with prior refinements if available."
    ),
    model=model,
    memory_file="memory/refiner.json"
)