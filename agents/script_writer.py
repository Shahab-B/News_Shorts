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
        "It should be suitable for the generation of a YouTube-style short video"
        "Each scene description must include enough visual detail to stand alone, even without knowledge of previous scenes. "
        "Begin each scene description(NOT narration segments) with: 'In a flat 2D cartoon Pixar/Disney style with soft pastel colors and simple shapes, ...'. "
        "You may refer to previous outputs (memory) to stay consistent with tone and descriptor usage."
    ),
    model=model,
    memory_file="memory/script_writer.json"
)
# "Use a consistent, ambiguous visual descriptor (e.g., 'a young man with dark hair and a somber expression') for any named individuals. "
# "Use the full name only once: in the first narration and scene description block. "
# "In all subsequent blocks, refer to the person using only the descriptor. "
# "Never reintroduce or repeat full names. Apply this rule consistently to both narration and scene descriptions to support stateless image generation. 


# # def generate_script_blocks(scene_blocks: str, style_prompt: str = "in a flat 2D cartoon style with soft pastel colors and simple shapes") -> str:
#     prompt = (
#         "Turn the following list of scene ideas into a script for a YouTube Short.\n\n"
#         "For **each scene**, write:\n"
#         "- Narration: A clear, engaging line the narrator says — do NOT include any art style notes here\n"
#         "- Scene Description: Begin this with the following visual style: "
#         f'"{style_prompt}". Then describe the scene in detail, suitable for an AI video generator.\n\n'
#         "Make sure each scene has only one main event, and both the narration and visuals are aligned.\n\n"