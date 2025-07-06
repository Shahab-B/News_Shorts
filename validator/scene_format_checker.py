import os
import re
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = os.getenv("GPT_MODEL")

def validate_scene_structure(script: str):
    """
    Checks if script is properly segmented into Narration/Scene Description blocks.
    Returns warnings for missing labels.
    """
    missing_narration = "Narration:" not in script
    missing_scene = "Scene Description:" not in script
    if missing_narration or missing_scene:
        issues = []
        if missing_narration:
            issues.append("Missing 'Narration:' labels.")
        if missing_scene:
            issues.append("Missing 'Scene Description:' labels.")
        return "Warning: " + " ".join(issues)
    return "Pass: Script format appears valid."

def extract_person_names(text: str) -> list[str]:
    """
    Uses GPT to extract full names of people from input text.
    """
    prompt = (
        "Extract the full names of all real or fictional people mentioned in the following text. "
        "Do not include places, organizations, or titles. Just list the names:\n\n"
        f"{text.strip()}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    names = response.choices[0].message.content.strip().splitlines()
    return [name.strip("-• ") for name in names if name.strip()]

def generate_descriptor(name: str) -> str:
    """
    Generates an ambiguous visual descriptor for a person using GPT.
    """
    prompt = (
        f"Create a consistent and ambiguous visual character descriptor for {name} "
        "suitable for visual storytelling. Avoid real-world identity references or surnames. "
        "For example: 'a young man with dark hair and a somber expression'."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def fix_descriptor_name_pairings(script: str, descriptor: str, name: str) -> str:
    """
    Cleans up scene description lines like 'descriptor, Name' or 'Name, descriptor',
    leaving just the descriptor.
    """
    lines = script.splitlines()
    fixed_lines = []

    last_name = name.split()[-1]
    first_name = name.split()[0]
    in_scene = False

    for line in lines:
        if line.strip().startswith("Scene Description:"):
            in_scene = True
        elif line.strip().startswith("Narration:"):
            in_scene = False

        if in_scene:
            # Descriptor, Name
            line = re.sub(
                rf"({re.escape(descriptor)}\s*,?\s*)({re.escape(first_name)}\s+)?{re.escape(last_name)}",
                r"\1",
                line,
                flags=re.IGNORECASE,
            )
            # Name, Descriptor
            line = re.sub(
                rf"({re.escape(first_name)}\s+)?{re.escape(last_name)}\s*,?\s*{re.escape(descriptor)}",
                descriptor,
                line,
                flags=re.IGNORECASE,
            )
        fixed_lines.append(line)

    return "\n".join(fixed_lines)

def auto_replace_name_leaks(script: str) -> str:
    """
    Replaces all person name mentions in Scene Descriptions with their descriptors,
    preserving narration as-is.
    """
    full_names = extract_person_names(script)
    descriptor_map = {name: generate_descriptor(name) for name in full_names}

    lines = script.splitlines()
    updated_lines = []

    in_scene = False
    for line in lines:
        if line.strip().startswith("Scene Description:"):
            in_scene = True
        elif line.strip().startswith("Narration:"):
            in_scene = False

        if in_scene:
            for name, descriptor in descriptor_map.items():
                last_name = name.split()[-1]
                if name in line:
                    line = line.replace(name, descriptor)
                elif last_name in line:
                    line = re.sub(rf"\b{last_name}\b", descriptor, line)
                # Final cleanup of "Name, descriptor" or vice versa
                line = fix_descriptor_name_pairings(line, descriptor, name)
        updated_lines.append(line)

    return "\n".join(updated_lines)

def check_descriptor_leaks(script: str, names: list[str]) -> list[str]:
    """
    Check if any original names are leaking into Scene Descriptions.
    Returns a list of leaked lines.
    """
    leaked = []
    for line in script.splitlines():
        if line.strip().startswith("Scene Description:"):
            for name in names:
                if name in line:
                    leaked.append(line)
    return leaked


def auto_fix_descriptor_leaks(script: str, name_descriptor_map: dict[str, str]) -> str:
    """
    Replaces any lingering name mentions in Scene Descriptions with their corresponding descriptors.
    """
    lines = script.splitlines()
    fixed_lines = []

    for line in lines:
        if line.strip().startswith("Scene Description:"):
            for name, descriptor in name_descriptor_map.items():
                full = name
                last = name.split()[-1]
                line = line.replace(full, descriptor)
                line = re.sub(rf'\b{re.escape(last)}\b', descriptor, line)
        fixed_lines.append(line)

    return "\n".join(fixed_lines)

