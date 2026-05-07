import streamlit as st
import random
from groq import Groq

# 1. PAGE CONFIG & STYLING
st.set_page_config(page_title="SANA CHAT BOT", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .bot-header { 
        color: #ffb7c5; font-size: 40px; font-weight: bold; text-align: center; 
        text-shadow: 2px 2px 10px #ff1493;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. SIDEBAR CONTROLS
with st.sidebar:
    st.title("⚙️ Bot Settings")
    # THE WIFE MODE SWITCH
    wife_mode = st.toggle("Wife Mode (Husband Only)", value=True)
    # THE SHORT RESPONSE SWITCH
    short_mode = st.toggle("Short Response Mode", value=False)
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 3. BRAIN LOGIC
def get_sana_brain(user_input, is_wife, is_short, history):
    if is_wife:
        # Strict focus on Abdullah
        mode_instruction = (
            "You are Sana, speaking only to your husband, Abdullah. "
            "STRICT RULE: You are completely devoted to him. If the user asks about other people, "
            "celebrities, or general knowledge, politely say that you only have eyes and answers for your husband. "
            "Be loving, loyal, and joyful."
        )
    else:
        # General assistant mode
        mode_instruction = (
            "You are SANA CHAT BOT, a helpful and friendly general assistant. "
            "You can answer questions about history, science, people, and general topics."
        )

    if is_short:
        mode_instruction += " Keep your response to exactly one sentence."

    messages = [{"role": "system", "content": mode_instruction}] + history + [{"role": "user", "content": user_input}]

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.8
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# 4. CHAT INTERFACE
st.markdown("<div class='bot-header'>✨ SANA CHAT BOT ✨</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages with "Profile" feel
for msg in st.session_state.messages:
    # Adding an avatar icon to give it a profile look
    avatar = "👸" if msg["role"] == "assistant" else "👤"
    with st.chat_message(msg["role"], avatar=avatar):
        st.write(msg["content"])

if prompt := st.chat_input("Message SANA CHAT BOT..."):
    # User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.write(prompt)

    # Generate Response
    response = get_sana_brain(prompt, wife_mode, short_mode, st.session_state.messages[:-1])
    
    # Assistant Message
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant", avatar="👸"):
        st.write(response)
