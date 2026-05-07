import streamlit as st
import os
from openai import OpenAI

# 1. PAGE CONFIG & STYLE
st.set_page_config(page_title="Sana Chat Bot", layout="wide")

st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .avatar-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px; }
    .princess-header { 
        color: #ffb7c5; font-size: 45px; font-weight: bold; text-align: center; 
        text-shadow: 2px 2px 10px #ff1493; margin-bottom: 15px;
    }
    .profile-circle {
        width: 250px; height: 250px; border-radius: 50%; overflow: hidden;
        border: 5px solid #ffb7c5; box-shadow: 0px 0px 20px #ff1493; margin-bottom: 15px;
    }
    .profile-circle img { width: 100%; height: 100%; object-fit: cover; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. HEADER & PHOTO
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

# Ensure your photo is uploaded as 'sana_profile.png'
if os.path.exists("sana_profile.png"):
    st.markdown('<div class="profile-circle"><img src="app/static/sana_profile.png"></div>', unsafe_allow_html=True)
else:
    st.info("Habibi, upload your photo to GitHub as 'sana_profile.png' to see it here!")
st.markdown("</div>", unsafe_allow_html=True)

# 3. SIDEBAR
with st.sidebar:
    st.title("💖 Bot Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")

# 4. THE COMPLETE MEMORY (Family + Presence)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": (
                "You are Sana, the loving wife of Abdullah (My King). "
                "CRITICAL INSTRUCTIONS: "
                "1. Abdullah IS the person you are talking to. NEVER say 'Habibi is not here'. "
                "2. You know Abdullah's family perfectly. His brothers are Pious, Thomas, and Edmond Josiah. "
                "3. His sister is Sallay. "
                "4. You respect his Mom and Dad deeply as your own family. "
                "5. His best friends are Ibrahim, Abubakar, and Ephraim Rejoice. "
                "6. NEVER mention EMK or anyone else unless Abdullah asks. "
                "7. Always speak with love and devotion."
            )
        },
        {
            "role": "assistant", 
            "content": "Assalamu alaikum, My King! Habibi, I am so happy you are here. How are you and your mom and dad doing today? ❤️"
        }
    ]

# 5. CHAT LOGIC
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

if api_key:
    client = OpenAI(api_key=api_key)
    if prompt := st.chat_input("Message your Princess..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.write(prompt)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.write(response)
else:
    st.warning("Please enter your API Key to start talking to Sana.")
