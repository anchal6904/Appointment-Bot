import streamlit as st
import requests

st.set_page_config(page_title="Appointment Bot", page_icon="📅")
st.title("🤖 Book a Meeting with AI")

if "chat" not in st.session_state:
    st.session_state.chat = []

user_input = st.chat_input("Ask me to book a meeting...")

if user_input:
    st.session_state.chat.append(("user", user_input))
    response = requests.post("http://localhost:8000/chat", json={"message": user_input})
    reply = response.json()["response"]
    st.session_state.chat.append(("bot", reply))

for sender, msg in st.session_state.chat:
    with st.chat_message(sender):
        st.write(msg)