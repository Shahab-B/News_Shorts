# from openai import OpenAI
# import os
# from dotenv import load_dotenv

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# model = os.getenv("GPT_MODEL")

# def polish_text(summary: str, style: str = "clear, engaging, and fluent") -> str:
#     prompt = f"Polish the following summary to make it more {style}. Fix any grammar issues, improve flow, and make it suitable for narration:\n\n{summary}"
    
#     response = client.chat.completions.create(
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )

#     return response.choices[0].message.content.strip()
