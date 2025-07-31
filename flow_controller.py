from agents.summarizer import summarizer
from agents.scene_planner import scene_planner
from agents.script_writer import script_writer
from agents.critic import critic
from agents.refiner import refiner
from agents.character_descriptor import character_descriptor
# from validator.scene_format_checker import (
#     auto_replace_name_leaks,
#     check_descriptor_leaks,
#     auto_fix_descriptor_leaks,
#     extract_person_names,
#     generate_descriptor
# )

# Load prompt templates
def load_prompt(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()
# def load_prompt(path: str) -> str:
#     with open(path) as f:
#         return f.read()

summarizer_prompt = load_prompt("prompts/summarizer.txt")
scene_planner_prompt = load_prompt("prompts/scene_planner.txt")
script_writer_prompt = load_prompt("prompts/script_writer.txt")
critic_prompt = load_prompt("prompts/critic.txt")
refiner_prompt = load_prompt("prompts/refiner.txt")
character_descriptor_prompt = load_prompt("prompts/character_descriptor.txt")

def run_pipeline(article_text):
    # Step 1: Summarization and scene planning
    summary = summarizer.run(article_text, summarizer_prompt)
    scenes = scene_planner.run(summary, scene_planner_prompt)
    script = script_writer.run(scenes, script_writer_prompt)

    # # Step 2: Extract names and generate descriptors
    # full_names = extract_person_names(article_text)
    # descriptor_map = {name: generate_descriptor(name, summary) for name in full_names}

    # Step 3: Critique + refinement
    critique = critic.run(script, critic_prompt)
    refined_script = refiner.run({"script": script, "feedback": critique}, refiner_prompt)

    # Step 3: Replace names with visual descriptors
    updated_script = character_descriptor.run(refined_script, character_descriptor_prompt)

    # # Step 4: Clean up names after refinement
    # final_cleaned = auto_replace_name_leaks(refined_script, descriptor_map)
    # leaks = check_descriptor_leaks(final_cleaned, full_names)
    # if leaks:
    #     final_cleaned = auto_fix_descriptor_leaks(final_cleaned, descriptor_map)

    return updated_script