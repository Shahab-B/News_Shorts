from agent_base import RoleAgent
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

summarizer = RoleAgent(
    name="Summarizer",
    goal=("You are a summarizer. Your job is to write concise, chronologically structured summaries in an informative tone. Refer to prior summaries for stylistic consistency when applicable."),
    model=model,
    memory_file="memory/summarizer.json"
)