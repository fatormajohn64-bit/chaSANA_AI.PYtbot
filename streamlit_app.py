import os
import subprocess
import sys

# 1. THE SELF-INSTALLER (Runs automatically if library is missing)
try:
    from audio_recorder_streamlit import audio_recorder
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "audio-recorder-streamlit"])
    # Re-import after installation
    from audio_recorder_streamlit import audio_recorder

import streamlit as st
from openai import OpenAI

# 2. Setup Page Configuration
st.set_page_config(page_title="sana cht bot", layout="wide")

# 3. Custom CSS (Dark Theme + Princess Glow)
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
    }
    .avatar-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        margin-top: 5px; 
    }
    .princess-header { 
        color: #ffb7c5; /* Soft Pink */
        font-size: 45px; 
        font-weight: bold; 
        text-align: center; 
        text-shadow: 2px 2px 10px #ff1493; /* Pink Glow */
        margin-bottom: 15px;
    }
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Header Section
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

# Image Handling (Ensure your image is named 'sana_bot.png' in the same folder)
image_path = "sana_bot.png"
if os.path.exists(image_path):
    st.image(image_path, width=280)
else:
    st.info("💡 Tip: Save Sana's picture as 'sana_bot.png' in your project folder to see her here.")
st.markdown("</div>", unsafe_allow_html=True)

# 5. Sidebar Settings
with st.sidebar:
    st.title("💖 Bot Settings")
    openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    voice_option = st.selectbox("Sana's Voice Style", ["nova", "shimmer", "alloy"], index=0)
    st.markdown("---")
    st.write("Using 'nova' for a sweet, natural voice.")

# 6. Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant", 
        "content": "Assalamu alaikum, how are you? My Habibi is not here right now, but I'm happy to chat with you. Is there something I can help you with?"
    }]

# Display messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 7. Logic for Input
if not openai_api_key:
    st.warning("Please add your API Key in the sidebar to start talking to Sana.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# Input Layout
st.write("---")
c1, c2 = st.columns([1, 4])

with c1:
    st.write("### 🎤 Speak")
    audio_bytes = audio_recorder(
        text="", 
        pause_threshold=2.0, 
        icon_size="3x", 
        icon_color="#ff1493"
    )

text_input = st.chat_input("Write something sweet...")

user_query = None

# Handle Voice Input
if audio_bytes:
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    with open("temp_audio.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        user_query = transcript.text

# Handle Text Input
elif text_input:
    user_query = text_input

# 8. Generating Response & Speaking Back
if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        # Text completion
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        full_response = chat_completion.choices[0].message.content
        st.markdown(full_response)

        # Text-to-Speech
        tts = client.audio.speech.create(
            model="tts-1",
            voice=voice_option,
            input=full_response
        )
        tts.stream_to_file("sana_speech.mp3")
        st.audio("sana_speech.mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
