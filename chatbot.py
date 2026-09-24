from google import genai
import os

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

print("Chatbot is ready! Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = client.models.generate_content(model="gemini-3.6-flash", contents=user_input)
    print("Bot:", response.text)