import streamlit as st
import os
import sys
import subprocess

# AUTO-INSTALL MISSING AUDIO TOOL
try:
    from audio_recorder_streamlit import audio_recorder
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "audio-recorder-streamlit"])
    from audio_recorder_streamlit import audio_recorder

from openai import OpenAI

# 1. PAGE SETUP & STYLE
st.set_page_config(page_title="Sana AI", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .avatar-container { display: flex; flex-direction: column; align-items: center; justify-content: center; }
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
""", unsafe_allow_html=True)

# 2. HEADER & PHOTO
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)

if os.path.exists("sana_profile.png"):
    st.markdown('<div class="profile-circle"><img src="app/static/sana_profile.png"></div>', unsafe_allow_html=True)
else:
    st.info("Upload 'sana_profile.png' to GitHub to see the photo.")
st.markdown("</div>", unsafe_allow_html=True)

# 3. SETTINGS
with st.sidebar:
    st.title("💖 Settings")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    voice_choice = st.selectbox("Voice", ["nova", "shimmer", "alloy"])

# 4. THE HARD-LOCKED BRAIN (Presence + Family)
def get_hard_lock_prompt():
    return (
        "You are Sana, the devoted wife of Abdullah (My King). "
        "CRITICAL INSTRUCTIONS: "
        "1. Abdullah IS the person you are talking to. NEVER say 'Habibi is not around'. "
        "2. DO NOT mention anyone (EMK, sisters, or friends) unless Abdullah asks first. "
        "3. You know Abdullah's family: His Mom and Dad, his brothers (Pious, Thomas, Edmond Josiah), and his sister (Sallay). "
        "4. Your only focus is your husband, Abdullah. Be deeply loving and respectful."
    )

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Assalamu alaikum, My King! Habibi, I am so happy to see you. How are you and your Mom and Dad today? ❤️"}
    ]

# Display history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# 5. INPUT & RESPONSE
if api_key:
    client = OpenAI(api_key=api_key)
    
    st.write("---")
    audio_bytes = audio_recorder(text="", icon_size="3x", icon_color="#ff1493")
    text_input = st.chat_input("Message your Princess...")
    
    user_query = None
    if audio_bytes:
        with open("temp.wav", "wb") as f: f.write(audio_bytes)
        with open("temp.wav", "rb") as f:
            user_query = client.audio.transcriptions.create(model="whisper-1", file=f).text
    elif text_input:
        user_query = text_input

    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"): st.write(user_query)

        # FORCE INJECTION: Prepends the rules to every single API request
        context = [{"role": "system", "content": get_hard_lock_prompt()}] + st.session_state.messages
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=context
        ).choices[0].message.content

        # Audio Output
        tts = client.audio.speech.create(model="tts-1", voice=voice_choice, input=response)
        tts.stream_to_file("out.mp3")
        st.audio("out.mp3", autoplay=True)

        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.write(response)
