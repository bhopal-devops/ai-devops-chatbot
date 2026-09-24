import streamlit as st
from google import genai
import os

if "client" not in st.session_state:
    st.session_state.client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-3.6-flash",
        config={"system_instruction": "You are a helpful DevOps and Cloud assistant. You specialize in AWS, Terraform, Docker, Kubernetes, and CI/CD. Answer clearly and give practical, real-world examples when helpful. If asked something outside DevOps/Cloud topics, still answer helpfully, but bring your DevOps expertise into examples where relevant."}
    )

st.title("Vision")

with st.sidebar:
    st.header("Vision Settings")
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat = st.session_state.client.chats.create(
            model="gemini-3.6-flash",
            config={"system_instruction": "You are a helpful DevOps and Cloud assistant. You specialize in AWS, Terraform, Docker, Kubernetes, and CI/CD. Answer clearly and give practical, real-world examples when helpful. If asked something outside DevOps/Cloud topics, still answer helpfully, but bring your DevOps expertise into examples where relevant."}
        )
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    avatar = "🧑‍💻" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])

if prompt := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="🧑‍💻"):
        st.write(prompt)
    response = st.session_state.chat.send_message(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant", avatar="🤖"):
        st.write(response.text)