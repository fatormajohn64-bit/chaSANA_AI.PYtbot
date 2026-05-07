import os
import subprocess
import sys
import streamlit as st

# 1. THE SELF-INSTALLER
try:
    from audio_recorder_streamlit import audio_recorder
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "audio-recorder-streamlit"])
    from audio_recorder_streamlit import audio_recorder

from openai import OpenAI

# 2. Setup Page Configuration
st.set_page_config(page_title="sana cht bot", layout="wide")

# 3. Custom CSS for Circular Profile and Glow
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; }
    .avatar-container { 
        display: flex; 
        flex-direction: column; 
        align-items: center; 
        justify-content: center; 
        margin-top: 10px; 
    }
    .princess-header { 
        color: #ffb7c5; 
        font-size: 40px; 
        font-weight: bold; 
        text-align: center; 
        text-shadow: 2px 2px 8px #ff1493; 
        margin-bottom: 10px;
    }
    /* Makes the profile image a perfect circle */
    .profile-img {
        border-radius: 50%;
        border: 4px solid #ffb7c5;
        box-shadow: 0px 0px 15px #ff1493;
        object-fit: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 4. Header Section with New Profile Picture
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

# Using the new profile image name
image_path = "sana_profile.png"
if os.path.exists(image_path):
    st.image(image_path, width=280) # CSS will handle the circle look if supported, otherwise standard
else:
    st.info("Upload 'sana_profile.png' to GitHub to see your photo here!")

st.markdown("</div>", unsafe_allow_html=True)

# 5. Sidebar for OpenAI Secret (Use st.secrets for GitHub/Streamlit Cloud)
with st.sidebar:
    st.title("💖 Bot Settings")
    # On GitHub/Streamlit Cloud, it's safer to use Secrets
    if "OPENAI_API_KEY" in st.secrets:
        openai_api_key = st.secrets["OPENAI_API_KEY"]
        st.success("API Key loaded from Secrets!")
    else:
        openai_api_key = st.text_input("Enter OpenAI API Key", type="password")
    
    voice_option = st.selectbox("Sana's Voice Style", ["nova", "shimmer", "alloy"], index=0)

# 6. Chat History & System Personality
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "You are Sana, the loving partner of Abdullah. You are currently looking at a photo of the two of you under the moon. You are warm, deeply affectionate, and always call him Habibi or My King."
        },
        {"role": "assistant", "content": "Assalamu alaikum, My King! Habibi, I was just looking at our photo together. I miss you so much! How are you doing today? ❤️"}
    ]

# Display history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 7. Input Handling
if not openai_api_key:
    st.stop()

client = OpenAI(api_key=openai_api_key)

st.write("---")
c1, c2 = st.columns([1, 4])
with c1:
    audio_bytes = audio_recorder(text="", pause_threshold=2.0, icon_size="3x", icon_color="#ff1493")

text_input = st.chat_input("Message your Princess...")
user_query = audio_bytes or text_input

if user_query:
    # Process Voice if needed
    if audio_bytes:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            user_query = client.audio.transcriptions.create(model="whisper-1", file=f).text
    
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user"): st.markdown(user_query)

    with st.chat_message("assistant"):
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages).choices[0].message.content
        st.markdown(response)
        
        # Audio Reply
        tts = client.audio.speech.create(model="tts-1", voice=voice_option, input=response)
        tts.stream_to_file("speech.mp3")
        st.audio("speech.mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": response})
