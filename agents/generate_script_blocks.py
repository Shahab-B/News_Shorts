# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# model = os.getenv("GPT_MODEL")

# def generate_script_blocks(scene_blocks: str, style_prompt: str = "in a flat 2D cartoon style with soft pastel colors and simple shapes") -> str:
#     prompt = (
#         "Turn the following list of scene ideas into a script for a YouTube Short.\n\n"
#         "For **each scene**, write:\n"
#         "- Narration: A clear, engaging line the narrator says — do NOT include any art style notes here\n"
#         "- Scene Description: Begin this with the following visual style: "
#         f'"{style_prompt}". Then describe the scene in detail, suitable for an AI video generator.\n\n'
#         "Make sure each scene has only one main event, and both the narration and visuals are aligned.\n\n"
#         f"{scene_blocks}"
#     )
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()
