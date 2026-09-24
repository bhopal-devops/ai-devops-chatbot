# Vision — AI DevOps Assistant Chatbot

A web-based AI chatbot built with Python, Streamlit, and Google's Gemini API. Specialized as a DevOps and Cloud assistant, with conversation memory, a custom personality, and a clean chat interface.

## Features

- Real-time conversation memory (remembers earlier messages in the session)
- Custom system personality focused on AWS, Terraform, Docker, Kubernetes, and CI/CD
- Chat-style UI with user/bot avatars
- Sidebar with a "Clear Chat" option to reset the conversation

## Tech Stack

- **Python** — core programming language
- **Streamlit** — turns the Python script into a browser-based web app
- **Google Gemini API** (`google-genai`) — powers the AI responses

---

## Part 1: Setup Commands (with explanations)

### 1. Create a virtual environment
```
python -m venv venv
```
This creates an isolated space for this project's Python packages, so they don't conflict with other projects on your system. Standard practice even in production codebases.

### 2. Activate the virtual environment
- Windows (PowerShell):
```
venv\Scripts\activate
```
- Mac/Linux:
```
source venv/bin/activate
```
This switches your terminal to use the isolated environment. You'll see `(venv)` appear at the start of your terminal line once active.

### 3. Install dependencies
```
pip install streamlit google-genai
```
Downloads and installs the two libraries this project depends on: Streamlit for the web interface, and Google's Gemini library for AI responses — installed only inside this project's virtual environment, not system-wide.

### 4. Set your Gemini API key
Get a free key from aistudio.google.com, then set it as an environment variable:
- Windows (PowerShell):
```
$env:GEMINI_API_KEY="your-actual-key-here"
```
- Mac/Linux:
```
export GEMINI_API_KEY="your-actual-key-here"
```
This stores your key temporarily in the terminal session, so the app can read it without the key ever being written directly into the code — a basic security practice that prevents secrets from being accidentally shared or committed to GitHub.

**Important:** an environment variable set in one terminal type (Command Prompt) does NOT carry over to a different terminal type (PowerShell) — each shell manages its own session variables independently. Set the key in the exact same terminal window you'll use to run the app.

### 5. Run the app
```
streamlit run app.py
```
This starts a local web server and automatically opens the chatbot in your browser at `http://localhost:8501`. Unlike a normal script (`python app.py`, which runs once and exits), Streamlit apps stay running continuously to serve a live webpage.

---

## Part 2: Code Walkthrough (line by line)

### Imports and client setup
```python
import streamlit as st
from google import genai
import os
```
Imports Streamlit (nicknamed `st`), Google's Gemini library, and Python's built-in `os` module (needed to read the API key from the environment, rather than hardcoding it in the file).

```python
if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
```
Creates the connection to Gemini using the API key. It's stored in `st.session_state` (Streamlit's way of remembering data across interactions) rather than a plain variable — this matters because Streamlit re-runs the entire script on every user action, and a plain variable would be recreated (and the old connection closed) every single time, breaking the chat.

### Chat session with personality
```python
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": "You are a helpful DevOps and Cloud assistant..."}
    )
```
`client.chats.create(...)` creates a special "Chat" object that automatically remembers the full conversation history internally — unlike calling the model directly, which treats every message as a brand-new, isolated request. The `system_instruction` shapes the bot's personality and expertise before any user conversation starts; it's invisible to the user but guides every response, the same way real production chatbots are given a specific role rather than being a blank general-purpose AI.

### Page title and sidebar
```python
st.title("Vision")
```
Displays the app's main heading.

```python
with st.sidebar:
    st.header("Vision Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.6-flash",
            config={"system_instruction": "..."}
        )
        st.rerun()
```
`with st.sidebar:` creates a collapsible panel on the left side of the page. `st.button(...)` creates a clickable button — the code inside the `if` only runs when it's clicked. Clicking "Clear Chat" resets both the visible message list AND creates a brand-new chat object — resetting only the display would leave the AI still "remembering" the old conversation internally. `st.rerun()` refreshes the page immediately so the empty chat shows right away.

### Message history and display
```python
if "messages" not in st.session_state:
    st.session_state.messages = []
```
Creates an empty list to store the full visible conversation (separate from the `chat` object, which manages what the AI remembers).

```python
for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
```
Loops through every stored message and displays it as a chat bubble, with a different emoji avatar depending on whether it came from the user or the bot.

### Handling new input
```python
if prompt := st.chat_input("Type your message..."):
```
Creates a text input box fixed at the bottom of the page. The walrus operator (`:=`) captures what the user typed into `prompt` and checks that they actually entered something, in one line.

```python
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)
```
Adds the user's message to the stored history, then immediately displays it.

```python
    response = st.session_state.chat.send_message(prompt)
```
Sends the message through the chat object (not a one-off model call), so it automatically includes prior conversation as context.

```python
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant", avatar="🤖"):
        st.write(response.text)
```
Stores and displays the bot's reply.

---

## What I Learned Building This

- Python's indentation isn't just style — it defines code structure. A misplaced indent silently broke the chat input box until I traced it line by line.
- Environment variables are scoped per terminal session — a variable set in Command Prompt isn't visible in PowerShell, and vice versa.
- Streamlit re-runs the entire script on every interaction, so anything that shouldn't be recreated each time (like an API client or chat session) must be stored in `session_state`.
- A `system_instruction` can give an AI model a consistent, specialized personality instead of a generic assistant.

## Roadmap

- [ ] Containerize the app with Docker
- [ ] Deploy to AWS using Terraform
- [ ] Migrate to Kubernetes (EKS)
