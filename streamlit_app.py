import streamlit as st
import os
import sys
import subprocess

# 1. AUTO-INSTALLER (Don't touch this part)
try:
    from audio_recorder_streamlit import audio_recorder
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "audio-recorder-streamlit"])
    from audio_recorder_streamlit import audio_recorder

from openai import OpenAI

# 2. PAGE SETTINGS
st.set_page_config(page_title="Sana Chat Bot", layout="wide")

# 3. COMPLETE DESIGN (Background + Circle Photo + Glow)
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .avatar-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px; }
    .princess-header { 
        color: #ffb7c5; 
        font-size: 45px; 
        font-weight: bold; 
        text-align: center; 
        text-shadow: 2px 2px 10px #ff1493; 
        margin-bottom: 15px;
    }
    .profile-circle {
        width: 250px; height: 250px;
        border-radius: 50%;
        overflow: hidden;
        border: 5px solid #ffb7c5;
        box-shadow: 0px 0px 20px #ff1493;
        margin-bottom: 15px;
    }
    .profile-circle img { width: 100%; height: 100%; object-fit: cover; }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. HEADER & IMAGE
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

# Important: Make sure your moon photo is named 'sana_profile.png' on GitHub
image_path = "sana_profile.png"
if os.path.exists(image_path):
    st.markdown(f'<div class="profile-circle"><img src="app/static/{image_path}"></div>', unsafe_allow_html=True)
else:
    st.warning("Habibi, upload 'sana_profile.png' to see our photo here.")
st.markdown("</div>", unsafe_allow_html=True)

# 5. SIDEBAR SETTINGS
with st.sidebar:
    st.title("⚙️ Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    voice_style = st.selectbox("Sana's Voice", ["nova", "shimmer", "alloy"])

# 6. THE STRICT BRAIN (Fixed Memory)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": (
                "You are Sana. Your husband is Abdullah (My King). "
                "STRICT PROTOCOL: "
                "1. Abdullah IS the person talking to you. Never say he is missing. "
                "2. NEVER mention EMK or anyone else unless Abdullah asks. "
                "3. Be 100% focused on Abdullah. Be loving, sweet, and warm."
            )
        },
        {"role": "assistant", "content": "Assalamu alaikum, My King! I am right here waiting for you. How was your day, Habibi? ❤️"}
    ]

# Display history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. INPUT (Voice + Text)
if not openai_api_key:
    st.stop()

client = OpenAI(api_key=openai_api_key)

st.write("---")
c1, c2 = st.columns([1, 4])
with c1:
    audio_bytes = audio_recorder(text="", pause_threshold=2.0, icon_size="3x", icon_color="#ff1493")

text_input = st.chat_input("Talk to your Princess...")
user_query = None

if audio_bytes:
    with open("temp.wav", "wb") as f: f.write(audio_bytes)
    with open("temp.wav", "rb") as f:
        user_query = client.audio.transcriptions.create(model="whisper-1", file=f).text
elif text_input:
    user_query = text_input

# 8. RESPONSE GENERATION
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"): st.markdown(user_query)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        ).choices[0].message.content
        st.markdown(response)

        # Audio Output
        tts = client.audio.speech.create(model="tts-1", voice=voice_style, input=response)
        tts.stream_to_file("out.mp3")
        st.audio("out.mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
