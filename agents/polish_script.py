# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# model = os.getenv("GPT_MODEL")

# def polish_script_scene_by_scene(full_script: str, style_prompt: str = "") -> str:
#     scene_blocks = full_script.split("\n\n")  # or regex split between scenes
#     polished_blocks = [polish_scene_block(block, style_prompt) for block in scene_blocks if block.strip()]
#     return "\n\n".join(polished_blocks)

# def polish_scene_block(scene_block: str, style_prompt: str = "") -> str:
#     prompt = (
#         "Polish the following YouTube Shorts script scene. Do not change the events or overall structure.\n\n"
#         "Keep these constraints:\n"
#         "- Keep the same narration and scene description format\n"
#         "- Enhance clarity, pacing, and emotional tone\n"
#         "- Do not add new characters, locations, or plot points\n"
#         "- Under 60 seconds of content"
#         "- Style: " + style_prompt + "\n\n"
#         f"{scene_block}"
#     )
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()
