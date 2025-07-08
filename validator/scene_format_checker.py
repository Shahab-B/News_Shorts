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

def generate_descriptor(name: str, context: str) -> str:
    """
    Generates a consistent, standalone visual character descriptor including gender, age,
    hair color, and expression. Informed by context.
    """
    prompt = (
        f"Given the following context, generate a full, repeatable visual descriptor for the person named {name}.\n\n"
        "The descriptor must include:\n"
        "- Gender\n"
        "- Approximate age (if known or implied)\n"
        "- Hair color\n"
        "- A defining facial expression or demeanor\n"
        "- No surnames or real-world identifiers\n\n"
        "It should be self-contained and usable repeatedly across different scenes.\n"
        "Example: 'a young man with dark hair and a somber expression'\n\n"
        f"Context:\n{context.strip()}\n\n"
        f"Descriptor for {name}:"
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

def auto_replace_name_leaks(script: str, name_descriptor_map: dict[str, str]) -> str:
    """
    Replaces all person name mentions in Scene Descriptions with their descriptors,
    covering full names, partial names, and possessives.
    """
    lines = script.splitlines()
    updated_lines = []
    in_scene = False

    for line in lines:
        if line.strip().startswith("Scene Description:"):
            in_scene = True
        elif line.strip().startswith("Narration:"):
            in_scene = False

        if in_scene:
            for name, descriptor in name_descriptor_map.items():
                parts = name.split()
                if len(parts) == 2:
                    first, last = parts
                    # Replace: full name and its possessive
                    line = re.sub(rf"\b{re.escape(name)}'s\b", f"{descriptor}'s", line, flags=re.IGNORECASE)
                    line = re.sub(rf"\b{re.escape(name)}\b", descriptor, line, flags=re.IGNORECASE)

                    # Replace: last name and its possessive
                    line = re.sub(rf"\b{re.escape(last)}'s\b", f"{descriptor}'s", line, flags=re.IGNORECASE)
                    line = re.sub(rf"\b{re.escape(last)}\b", descriptor, line, flags=re.IGNORECASE)

                    # Replace: first name and its possessive
                    line = re.sub(rf"\b{re.escape(first)}'s\b", f"{descriptor}'s", line, flags=re.IGNORECASE)
                    line = re.sub(rf"\b{re.escape(first)}\b", descriptor, line, flags=re.IGNORECASE)
                else:
                    # Single-name fallback
                    line = re.sub(rf"\b{re.escape(name)}'s\b", f"{descriptor}'s", line, flags=re.IGNORECASE)
                    line = re.sub(rf"\b{re.escape(name)}\b", descriptor, line, flags=re.IGNORECASE)

                # Clean pairings like "descriptor, Name" or "Name, descriptor"
                line = fix_descriptor_name_pairings(line, descriptor, name)

        updated_lines.append(line)

    return "\n".join(updated_lines)

def check_descriptor_leaks(script: str, names: list[str]) -> list[str]:
    """
    Checks if any original names (or possessives) leak into Scene Descriptions.
    Returns a list of lines where a name leak is detected.
    """
    leaked = []

    for line in script.splitlines():
        if not line.strip().startswith("Scene Description:"):
            continue

        # Normalize smart quotes to ASCII
        line = line.replace("’s", "'s").replace("‘", "'").replace("’", "'")

        for name in names:
            parts = name.split()
            first, last = parts[0], parts[-1]

            # Check for full name or possessive (e.g., "Wess Roley", "Wess Roley's")
            patterns = [
                rf"\b{re.escape(name)}('?s)?\b",
                rf"\b{re.escape(first)}('?s)?\b",
                rf"\b{re.escape(last)}('?s)?\b"
            ]

            for pattern in patterns:
                if re.search(pattern, line, flags=re.IGNORECASE):
                    leaked.append(line)
                    break  # No need to check more names in this line

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

