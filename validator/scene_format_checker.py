import re
from openai import OpenAI
import os
from dotenv import load_dotenv

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

def check_descriptor_leaks(script: str) -> list[str]:
    """
    Checks for name leaks or descriptor + name mixes in Scene Descriptions.
    Extracts all person names and flags improper reuse.
    """
    persons = extract_person_names(script)
    descriptors = {name: generate_descriptor(name) for name in persons}
    lines = script.splitlines()
    issues = []

    for i, line in enumerate(lines):
        if not line.strip().startswith("Scene Description:"):
            continue

        for full_name in persons:
            descriptor = descriptors[full_name]
            name_parts = full_name.split()
            first_name, last_name = name_parts[0], name_parts[-1]

            # Leak 1: full name appears after intro
            if re.search(rf"\b{re.escape(full_name)}\b", line):
                issues.append(f"Line {i+1}: Full name used in Scene Description after intro → {line.strip()}")

            # Leak 2: last or first name alone
            elif re.search(rf"\b({re.escape(first_name)}|{re.escape(last_name)})\b", line):
                issues.append(f"Line {i+1}: Partial name used in Scene Description → {line.strip()}")

            # Leak 3: descriptor + name combo
            elif re.search(rf"{re.escape(descriptor)}\s*,?\s*({re.escape(first_name)}|{re.escape(last_name)}|{re.escape(full_name)})", line):
                issues.append(f"Line {i+1}: Descriptor+name mix → {line.strip()}")

    return issues

def extract_person_names(text: str) -> list[str]:
    """
    Uses GPT to extract all full names of people mentioned in the input text.
    """
    prompt = (
        "Extract all full names of people mentioned in the following text. "
        "Return only names of people in a list format, without additional comments:\n\n"
        f"{text.strip()}"
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    names = response.choices[0].message.content.strip().splitlines()
    return [name.strip("-• ") for name in names if name.strip()]

def fix_descriptor_name_pairings(script: str, descriptor: str, name: str) -> str:
    """
    Removes name pairings like 'descriptor, Name' or 'Name, descriptor' in scene descriptions.
    Keeps only the descriptor for consistency with visual generation.
    """
    lines = script.splitlines()
    fixed_lines = []

    full_name = name
    last_name = name.split()[-1]
    first_name = name.split()[0]

    # Regex to match any line starting with "Scene Description:"
    in_scene = False

    for line in lines:
        if line.strip().startswith("Scene Description:"):
            in_scene = True
        elif line.strip().startswith("Narration:"):
            in_scene = False

        if in_scene:
            # Remove ", Name" following descriptor
            line = re.sub(
                rf"({re.escape(descriptor)})\s*,?\s*({re.escape(first_name)}\s+)?{re.escape(last_name)}",
                r"\1",
                line,
                flags=re.IGNORECASE,
            )
            # Remove "Name, descriptor"
            line = re.sub(
                rf"({re.escape(first_name)}\s+)?{re.escape(last_name)}\s*,?\s*{re.escape(descriptor)}",
                descriptor,
                line,
                flags=re.IGNORECASE,
            )
        fixed_lines.append(line)

    return "\n".join(fixed_lines)

def generate_descriptor(name: str) -> str:
    """
    Use GPT to generate a consistent but ambiguous visual descriptor for a person.
    """
    prompt = (
        f"Create a visually descriptive but ambiguous character descriptor for {name}. "
        "Avoid specific references to real-world identity or actions. Use a tone suitable "
        "for visual storytelling (e.g., 'a person named X with...')."
    )
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()


def auto_replace_name_leaks(script: str) -> str:
    """
    Replaces full names and last names in Scene Descriptions only after their first mention.
    Descriptors are generated once per person using GPT.
    Cleans up combos like "the young man, Wess Roley" → just the descriptor.
    """
    persons = extract_person_names(script)
    descriptors = {name: generate_descriptor(name) for name in persons}

    seen = set()
    lines = script.splitlines()
    updated_lines = []

    for line in lines:
        updated_line = line

        for full_name in persons:
            descriptor = descriptors[full_name]
            name_parts = full_name.split()
            first_name = name_parts[0]
            last_name = name_parts[-1]

            # First mention? Let it through
            if any(re.search(rf"\b{re.escape(part)}\b", updated_line) for part in [full_name, last_name, first_name]):
                if full_name not in seen:
                    seen.add(full_name)
                    continue  # Allow name on first use

            # Only rewrite inside Scene Descriptions
            if updated_line.strip().startswith("Scene Description:"):
                # Remove patterns like: "the descriptor, Wess", "the descriptor, Roley", etc.
                updated_line = re.sub(
                    rf"{re.escape(descriptor)}\s*,?\s*(\b{re.escape(full_name)}\b|\b{re.escape(first_name)}\b|\b{re.escape(last_name)}\b)",
                    descriptor,
                    updated_line
                )
                # Replace standalone full, last, or first name
                updated_line = re.sub(rf"\b{re.escape(full_name)}\b", descriptor, updated_line)
                updated_line = re.sub(rf"\b{re.escape(last_name)}\b", descriptor, updated_line)
                updated_line = re.sub(rf"\b{re.escape(first_name)}\b", descriptor, updated_line)

        updated_lines.append(updated_line)

    return "\n".join(updated_lines)
