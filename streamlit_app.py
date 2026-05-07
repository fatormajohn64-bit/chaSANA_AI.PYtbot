import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import os

# 1. Setup Page Configuration
st.set_page_config(page_title="sana cht bot", layout="wide")

st.markdown(
    """
    <style>
    .avatar-container { display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 10px; }
    .princess-header { color: white; font-size: 40px; font-weight: bold; text-align: center; margin-bottom: 5px; }
    </style>
    """,
    unsafe_allow_html=True
)

# 2. Header with Sana's Face
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)
st.markdown("<div class='princess-header'>★彡[ PŘIŇCĚŜŜ 👸 ]彡★</div>", unsafe_allow_html=True)
image_path = "sana_bot.png"
if os.path.exists(image_path):
    st.image(image_path, width=250)
st.markdown("</div>", unsafe_allow_html=True)

# 3. Sidebar Settings
with st.sidebar:
    st.title("Settings")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    voice_option = st.selectbox("Sana's Voice", ["nova", "shimmer", "alloy"])

# 4. Chat logic
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Assalamu alaikum, how are you? My Habibi is not here right now, but I'm happy to chat with you."}]

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. VOICE INPUT SECTION
st.write("---")
st.write("### 🎤 Speak to Sana")
audio_bytes = audio_recorder(text="Click to speak...", pause_threshold=2.0, icon_size="2x")

if not openai_api_key:
    st.warning("Please enter your API Key in the sidebar.")
    st.stop()

client = OpenAI(api_key=openai_api_key)

# If voice is recorded
if audio_bytes:
    # Save audio to temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes)
    
    # Transcribe (Speech-to-Text)
    with open("temp_audio.wav", "rb") as audio_file:
        transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
        user_text = transcript.text

    # Add user message to chat
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    # Generate AI Response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        full_response = response.choices[0].message.content
        st.markdown(full_response)

        # Generate Audio (Text-to-Speech)
        audio_response = client.audio.speech.create(
            model="tts-1",
            voice=voice_option,
            input=full_response
        )
        audio_response.stream_to_file("response.mp3")
        st.audio("response.mp3", autoplay=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Also allow typing
if prompt := st.chat_input("Or type to your Princess..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    # ... (Response logic for typing) ...
