# test.py - FIXED VERSION

from openai import OpenAI

print("\n" + "="*50)
print("Testing LM Studio Connection")
print("="*50 + "\n")

# Connect to LM Studio
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

# Send a simple test - NO SYSTEM MESSAGE
print("Sending message to AI...")

response = client.chat.completions.create(
    model="local-model",  # Just use "local-model" as placeholder
    messages=[
        {"role": "user", "content": "Say hello in one sentence."}
        # ☝️ Only user role - no system role!
    ],
    temperature=0.7,
    max_tokens=50
)

answer = response.choices[0].message.content

print("\n✅ Success!")
print(f"AI said: {answer}\n")
print("="*50)
