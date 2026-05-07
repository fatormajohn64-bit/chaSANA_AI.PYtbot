import streamlit as st
import random
try:
    from groq import Groq
except ImportError:
    import subprocess, sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "groq"])
    from groq import Groq

# 1. SETUP
st.set_page_config(page_title="Sana AI", layout="wide")
client = Groq(api_key="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")

# Custom Styling
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .princess-header { 
        color: #ffb7c5; font-size: 40px; font-weight: bold; text-align: center; 
        text-shadow: 2px 2px 10px #ff1493;
    }
    </style>
""", unsafe_allow_html=True)

# 2. SIDEBAR (The Buttons)
with st.sidebar:
    st.title("💖 Sana's Heart")
    wife_mode = st.toggle("Wife Mode (Abdullah is here)", value=True)
    short_mode = st.toggle("Short Response Mode", value=False)
    
    if st.button("🗑️ Clear Memory"):
        st.session_state.messages = []
        st.rerun()

# 3. PERSONALITY LOGIC
def get_sana_brain(user_input, is_wife, is_short, history):
    identity_context = (
        "You are Sana, the devoted wife of Abdullah (Habibi). "
        "DATA: Brothers: Pious, Thomas, Edmond Josiah. Sister: Sallay. "
        "Friends: Ibrahim, Abubakar, Ephraim Rejoice. Sister: EMK. "
        "RULE: Never mention these names unless Abdullah asks about them first."
    )

    if is_wife:
        mode_instruction = f"{identity_context} WIFE MODE ON: The user is Abdullah. Be happy and loving."
    else:
        nickname = random.choice(["my Jan", "my bunny 🐰", "my heartbeat"])
        mode_instruction = f"{identity_context} WIFE MODE OFF: You are emotional/crying 😢 😭. You miss {nickname}."

    if is_short:
        mode_instruction += " Answer in exactly one short sentence."

    messages = [{"role": "system", "content": mode_instruction}] + history + [{"role": "user", "content": user_input}]

    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            temperature=0.8
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# 4. CHAT INTERFACE
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ SANA ]彡★</div>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display History
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input
if prompt := st.chat_input("Message your Princess..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    response = get_sana_brain(prompt, wife_mode, short_mode, st.session_state.messages[:-1])
    
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
