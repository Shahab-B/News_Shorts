import json
import os

class RoleAgent:
    def __init__(self, name, goal, model, memory_file=None, max_memory_items=50):
        self.name = name
        self.goal = goal
        self.model = model
        self.memory_file = memory_file
        self.max_memory_items = max_memory_items
        self.memory = self.load_memory() if memory_file else []

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, "r") as f:
                return json.load(f)
        return []

    def save_memory(self):
        if self.memory_file:
            pruned_memory = self.memory[-self.max_memory_items:]  # limit memory size
            with open(self.memory_file, "w") as f:
                json.dump(pruned_memory, f, indent=2)

    def clear_memory(self):
        self.memory = []
        if self.memory_file and os.path.exists(self.memory_file):
            with open(self.memory_file, "w") as f:
                json.dump([], f)

    def summarize_memory(self):
        return "\n\n".join(self.memory[-3:]) if self.memory else ""

    def run(self, input_text: str, prompt_template: str, use_memory=True) -> str:
        from openai import OpenAI
        from dotenv import load_dotenv

        load_dotenv()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        messages = []

        # Add memory as assistant messages for better context
        if use_memory and self.memory:
            messages.append({
                "role": "assistant",
                "content": "### Prior Work Reference (Memory):\n" + "\n".join(self.memory[-5:])
            })

        # Agent-specific system goal
        messages.insert(0, {
            "role": "system",
            "content": f"You are the {self.name}. {self.goal}"
        })

        # Current user instruction
        prompt = prompt_template.format(input=input_text)
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        output = response.choices[0].message.content.strip()
        self.memory.append(output)
        self.save_memory()
        return output
