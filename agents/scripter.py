# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# model = os.getenv("GPT_MODEL")

# def generate_script(summary: str, format: str = "short YouTube-style video") -> str:
#     prompt = (
#         f"Turn the following polished summary into a {format} script. Guiding the user through the events that transpired. Include a strong hook, "
#         "narration, and scene suggestions for a video to coincide alongside the narration.:\n\n" + summary # Multiple scene descriptions each of a single event and have an associated narration segment
#     )

#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content.strip()
