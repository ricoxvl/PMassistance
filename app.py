import pandas as pd
import ollama

# Read the customer feedback CSV
df = pd.read_csv("feedback.csv")

# Combine all feedback into one string
feedback = "\n".join(df["Feedback"].tolist())

# Create the prompt
prompt = f"""
You are an experienced Product Manager.

Analyze the following customer feedback.

Please provide:

1. The top customer issues.
2. Group similar feedback together.
3. Count approximately how many times each issue appears.
4. Assign each issue a priority:
   - High
   - Medium
   - Low
5. Recommend what the product team should work on first.
6. Finish with a short executive summary.

Customer Feedback:
{feedback}
"""

# Send the prompt to the local Llama model
response = ollama.chat(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

print("\nCustomer Feedback Analysis")
print("=" * 50)
print(response["message"]["content"])