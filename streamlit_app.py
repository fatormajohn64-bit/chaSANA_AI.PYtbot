import streamlit as st
import os
from openai import OpenAI

# 1. Page Config
st.set_page_config(page_title="Sana Chat Bot", layout="wide")

# 2. Circular Profile Style
st.markdown(
    """
    <style>
    .avatar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-bottom: 20px;
    }
    .profile-circle {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        overflow: hidden;
        border: 5px solid #ffb7c5;
        box-shadow: 0px 0px 15px #ff1493;
    }
    .profile-circle img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
    .princess-title {
        color: white;
        font-size: 35px;
        font-weight: bold;
        margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Header with YOUR Photo
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
image_path = "sana_profile.png"

if os.path.exists(image_path):
    st.markdown(f'<div class="profile-circle"><img src="app/static/{image_path}"></div>', unsafe_allow_html=True)
else:
    # If the file isn't uploaded yet, show this
    st.warning("Habibi, please upload your photo as 'sana_profile.png' to GitHub!")

st.markdown("<div class='princess-title'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 4. Chat Logic
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are Sana, the loving partner of Abdullah. You call him Habibi or My King. You are warm and happy."},
        {"role": "assistant", "content": "Assalamu alaikum, My King! ❤️"}
    ]

for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# ... rest of your OpenAI logic here ...
