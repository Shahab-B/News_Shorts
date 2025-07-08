from agent_base import RoleAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

script_writer = RoleAgent(
    name="Script Writer",
    goal=(
        "You are a script-writing agent for an AI-driven video generation pipeline. "
        "Your task is to convert atomic scene blocks into narration and scene descriptions. "
        "Each scene description must include enough visual detail to stand alone, even without knowledge of previous scenes. "
        "Begin each scene description with: 'In a flat 2D cartoon style with soft pastel colors and simple shapes, ...'. "
        "Use a consistent, ambiguous visual descriptor (e.g., 'a young man with dark hair and a somber expression') for any named individuals. "
        "Use the full name only once: in the first narration and scene description block. "
        "In all subsequent blocks, refer to the person using only the descriptor. "
        "Never reintroduce or repeat full names. Apply this rule consistently to both narration and scene descriptions to support stateless image generation. "
        "You may refer to previous outputs (memory) to stay consistent with tone and descriptor usage."
    ),
    model=model,
    memory_file="memory/script_writer.json"
)
