from agents.summarizer import summarizer
from agents.scene_planner import scene_planner
from agents.script_writer import script_writer
from agents.critic import critic
from agents.refiner import refiner
from agents.character_descriptor import character_descriptor

def erase_agent_memory():
    summarizer.clear_memory()
    scene_planner.clear_memory()
    script_writer.clear_memory()
    critic.clear_memory()
    refiner.clear_memory()
    character_descriptor.clear_memory()

erase_agent_memory()