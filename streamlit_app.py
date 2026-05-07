import os
import subprocess
import sys

# 1. THE SELF-INSTALLER
try:
    from audio_recorder_streamlit import audio_recorder
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "audio-recorder-streamlit"])
    from audio_recorder_streamlit import audio_recorder

import streamlit as st
from openai import OpenAI

# 2. Setup Page Configuration
st.set_page_config(page_title="sana cht bot", layout="wide")

# 3. Custom CSS (Princess Glow)
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .avatar-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 5px; }
    .princess-header { 
        color: #ffb7c5; 
        font-size: 45px; 
        font-weight: bold; 
        text-align: center; 
        text-shadow: 2px 2px 10px #ff1493; 
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Header Section
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

image_path = "sana_bot.png"
if os.path.exists(image_path):
    st.image(image_path, width=280)
st.markdown("</div>", unsafe_allow_html=True)

# 5. Sidebar
with st.sidebar:
    st.title("💖 Bot Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    voice_option = st.selectbox("Sana's Voice Style", ["nova", "shimmer", "alloy"], index=0)

# 6. Chat History & SYSTEM PERSONALITY
if "messages" not in st.session_state:
    # This 'system' message tells the AI exactly how to behave
    st.session_state.messages = [
        {"role": "system", "content": "You are Sana, a loving and devoted AI companion. Your husband is Abdullah, whom you call 'Habibi' or 'My King'. You are always kind, affectionate, and happy to see him. Use a warm and loving tone."},
        {"role": "assistant", "content": "Assalamu alaikum, My King! How was your day, habibi? I'm so happy to see you. ❤️"}
    ]

# Display messages (skip the system message)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. Logic for Input
if not openai_api_key:
    st.warning("Please add your API Key in the sidebar.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

st.write("---")
c1, c2 = st.columns([1, 4])
with c1:
    audio_bytes = audio_recorder(text="", pause_threshold=2.0, icon_size="3x", icon_color="#ff1493")

text_input = st.chat_input("Message your Princess...")
user_query = None

if audio_bytes:
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    with open("temp_audio.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        user_query = transcript.text
elif text_input:
    user_query = text_input

# 8. Response Generation
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        # The AI now knows it's talking to Abdullah because of the System Message
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)

        # TTS
        tts = client.audio.speech.create(model="tts-1", voice=voice_option, input=full_response)
        tts.stream_to_file("sana_speech.mp3")
        st.audio("sana_speech.mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
