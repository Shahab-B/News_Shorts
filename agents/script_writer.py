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
        "Convert atomic scene blocks into narration and scene descriptions. "
        "Each scene description must include enough visual detail to stand alone, even without knowledge of previous scenes. "
        "Start each scene description with 'In a flat 2D cartoon style with soft pastel colors and simple shapes, ...'. "
        "Automatically identify named individuals (e.g., Wess Roley) and assign them a consistent, ambiguous visual descriptor (e.g., 'a young man with dark hair and a somber expression'). "
        "Use the character's full name only in the first narration and scene description block. In all subsequent blocks, refer to the character using only the descriptor. "
        "Apply this rule to both narration and scene descriptions to ensure consistency and coherence in stateless AI video generation."
        "Strictly enforce that names do not appear more than once after initial introduction."
    ),
    model=model,
    memory_file="memory/script_writer.json"
)
