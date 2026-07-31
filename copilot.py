import json
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.1-8b-instant"


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

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content