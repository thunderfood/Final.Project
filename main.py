# main.py - AI PC Health Analyzer (FIXED)

from openai import OpenAI
import sys
sys.path.append('src')

from tools.system_monitor import get_system_report

print("\n" + "="*60)
print("AI PC Health Analyzer")
print("="*60 + "\n")

# Step 1: Get system report
print("📊 Checking your PC...")
system_report = get_system_report()
print(system_report)

# Step 2: Connect to AI
print("\n🤖 Asking AI to analyze...\n")

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="not-needed"
)

# Step 3: Ask AI to analyze - Combine instruction into user message
prompt = f"""You are a PC health expert. Analyze this system report and provide:

1. Overall Status (one word: Good/Warning/Critical)
2. Main Issues (if any)
3. Top Recommendation (one action to take)

Keep it brief and clear.

REPORT:
{system_report}

FORMAT:
Status: [Good/Warning/Critical]
Issues: [list or "None"]
Action: [one recommendation]"""

response = client.chat.completions.create(
    model="local-model",
    messages=[
        {"role": "user", "content": prompt}  # All in user message
    ],
    temperature=0.7,
    max_tokens=200
)

analysis = response.choices[0].message.content

print("="*60)
print("AI ANALYSIS:")
print("="*60)
print(analysis)
print("="*60 + "\n")

print("✅ Analysis complete!\n")
