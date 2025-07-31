# agents/character_descriptor_agent.py
from agent_base import RoleAgent
import os
from dotenv import load_dotenv

load_dotenv()
model = os.getenv("GPT_MODEL")

character_descriptor = RoleAgent(
    name="Character Descriptor",
    goal=(
        "Identify all distinct, singular people mentioned in the story — including relational references like 'Wess Roley's grandfather'. "
        "Generate a consistent, self-contained visual descriptor for each person that includes gender, approximate age (if implied), hair color, "
        "and defining expression or demeanor. Descriptors must be specific, visual, and repeatable across scenes. "
        "Only apply descriptors to **clearly individual humans**. "
        "**DO NOT** create descriptors for group-based or generic roles such as: "
        "'police officers', 'firefighters', 'law enforcement', 'authorities', 'officials', 'emergency responders', 'paramedics', etc. "
        "Leave all such generic roles unchanged in Scene Descriptions. "
        "Then, in **Scene Descriptions only**, replace every reference to these individuals — full names, first names, last names, relational phrases, and possessives — "
        "with their full visual descriptor. "
        "Do NOT preserve or wrap the original name — fully substitute it. "
        "Avoid possessive structures on descriptors (e.g., 'a tall man's coat') — instead restructure the sentence (e.g., 'the coat of a tall man'). "
        "Never use pronouns or vague terms like 'the character'. "
        "Do not rewrite or replace generic roles — leave them exactly as they appear. "
        "Narration blocks must remain completely unmodified. "
        "Ensure each Scene Description is self-contained and visually clear without relying on prior scenes."
    ),
    model=model,
    memory_file="memory/character_descriptor.json"
)

