import ollama
from prompts import PROMPT


def analyze_resume(resume_text):

    prompt = PROMPT.format(resume=resume_text)

    response = ollama.chat(
        model="Qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]