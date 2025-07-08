from agents.summarizer import summarizer
from agents.scene_planner import scene_planner
from agents.script_writer import script_writer
from agents.critic import critic
from agents.refiner import refiner
from validator.scene_format_checker import (
    auto_replace_name_leaks,
    check_descriptor_leaks,
    auto_fix_descriptor_leaks,
    extract_person_names,
)

# Load prompt templates
def load_prompt(path: str) -> str:
    with open(path) as f:
        return f.read()

summarizer_prompt = load_prompt("prompts/summarizer.txt")
scene_planner_prompt = load_prompt("prompts/scene_planner.txt")
script_writer_prompt = load_prompt("prompts/script_writer.txt")
critic_prompt = load_prompt("prompts/critic.txt")
refiner_prompt = load_prompt("prompts/refiner.txt")

def run_pipeline(article_text):
    summary = summarizer.run(article_text, summarizer_prompt)
    scenes = scene_planner.run(summary, scene_planner_prompt)
    script = script_writer.run(scenes, script_writer_prompt)

    # Replace names with descriptors
    cleaned_script = auto_replace_name_leaks(script)

    # Auto-fix leaks if detected
    full_names = extract_person_names(article_text)
    leaks = check_descriptor_leaks(cleaned_script, full_names)
    if leaks:
        cleaned_script = auto_fix_descriptor_leaks(cleaned_script, full_names)

    # Proceed with critique and refinement
    critique = critic.run(cleaned_script, critic_prompt)
    refined = refiner.run({"script": cleaned_script, "feedback": critique}, refiner_prompt)

    return refined