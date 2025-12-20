import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print(f"Checking models for key ending in ...{api_key[-4:]}")

# List of common model names to test
candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-latest",
    "gemini-pro",
    "gemini-1.0-pro"
]

print("\n🔎 Testing candidates...")
found = False

for model_name in candidates:
    try:
        print(f"Testing: {model_name}...", end=" ")
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print("✅ WORKS!")
        print(f"\n🎉 USE THIS MODEL NAME: {model_name}")
        found = True
        break
    except Exception as e:
        print("❌")

if not found:
    print("\n⚠️ No common names worked. Printing ALL available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f" - {m.name}")