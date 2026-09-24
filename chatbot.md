# Gemini Python Code Explanation

## 1. Import Gemini Package

```python
import google.generativeai as genai
```

This imports the Gemini package we installed in Step 5, so our Python file can use it. We're giving it a shorter nickname, `genai`, so we don't have to type the full name every time we use it.

---

## 2. Import OS Module

```python
import os
```

`os` is a built-in Python module that lets our code interact with the operating system — we specifically need it to read the environment variable (your API key).

---

## 3. Configure Gemini API Key

```python
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
```

`os.environ["GEMINI_API_KEY"]` — this reads the environment variable you set earlier, fetching your actual API key value.

`genai.configure(api_key=...)` — this tells the Gemini package, "here's the key to use whenever you talk to Google's servers."

---

## 4. Create Gemini Model

```python
model = genai.GenerativeModel("gemini-1.5-flash")
```

This creates a "model" object — think of it as opening a connection to a specific AI model. We're choosing `gemini-1.5-flash`, which is fast and included in the free tier.

---

## 5. Print Chatbot Ready Message

```python
print("chatbot is ready! Type 'exit' to quit.")
```

This just prints a message to the screen once, so you know the program started correctly. `print()` is a built-in Python function that displays text.

---

## 6. Start the Loop

```python
while True:
```

This starts a loop that repeats forever, until we explicitly tell it to stop. This is what lets you have a back-and-forth conversation instead of the program running once and closing.

---

## 7. Get User Input

```python
user_input = input("You: ")
```

`input("You: ")` — displays `"You: "` on screen and waits for you to type something and press Enter.

`user_input =` — stores whatever you typed into a variable named `user_input`, so we can use it in the next lines.

---

## 8. Check for Exit

```python
if user_input.lower() == "exit":
```

This checks whether the user typed `"exit"`.

`user_input.lower()` converts the user's input to lowercase, so `EXIT`, `Exit`, or `exit` will all be treated as `exit`.


Step 1: Replace how we connect to Gemini

Find this line in your app.py:

python
client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

Right after it, add this new line:

python
if "chat" not in st.session_state:
    st.session_state.chat = client.chats.create(model="gemini-3.6-flash")


client.chats.create(model="gemini-3.6-flash") — this creates a special "Chat" object that automatically remembers the full conversation history internally, unlike generate_content which treats each call as a fresh, isolated request
We store it in st.session_state.chat (same memory technique as your messages list) so it persists across the entire session, not just one message

Step 2: Update how we send messages

Find this line:

python
response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)

Replace it with:

python
response = st.session_state.chat.send_message(prompt)

What changed: Instead of calling the model directly and getting a one-off response, we're now sending the message through the chat object we created — this automatically includes all previous messages as context, so the bot can reference things you said earlier in the conversation.

Make these two changes, save, and test it — try saying something like "My name is Bhopal" in one message, then in the next message ask "What's my name?" If it remembers, the feature is working.