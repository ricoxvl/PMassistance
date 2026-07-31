import json
import ollama

MODEL = "llama3.1:8b"


def ask_copilot(question, analysis):

    prompt = f"""
You are an experienced Senior Product Manager.

You have already analyzed customer feedback.

Analysis:

{json.dumps(analysis, indent=2)}

The user asks:

{question}

Answer like a Senior Product Manager.

Be specific and use the analysis above.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]