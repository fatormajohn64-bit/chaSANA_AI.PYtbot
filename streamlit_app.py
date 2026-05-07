import streamlit as st
from openai import OpenAI
import os

# 1. Setup Page Configuration
st.set_page_config(page_title="sana cht bot", layout="wide")

# 2. Add custom CSS to center the image and title
st.markdown(
    """
    <style>
    .avatar-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 2rem;
        margin-bottom: 2rem;
    }
    .custom-title {
        font-family: sans-serif;
        font-size: 2.5rem;
        font-weight: bold;
        margin-top: 1rem;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 3. Handle the Image and Title Display
st.markdown("<div class='avatar-container'>", unsafe_allow_html=True)

# Path to the image file (adjust if necessary)
image_filename = "sana_avatar.png"

# Check if the file exists before trying to display it
if os.path.exists(image_filename):
    st.image(image_filename, width=200) # Displays the image centered
else:
    # Fallback if image isn't found
    st.warning(f"Image not found. Please ensure '{image_filename}' is in the same folder.")
    st.image("https://via.placeholder.com/200?text=Sana+Avatar", width=200)

# Display the title below the image
st.markdown("<div class='custom-title'>sana cht bot</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True) # Close container div


# 4. Create Tabs for the rest of the application
tab1, tab2 = st.tabs(["Settings", "Chat Interface"])

with tab1:
    st.header("Configuration")
    st.write("Provide your OpenAI API key to start chatting.")
    openai_api_key = st.text_input("OpenAI API Key", type="password")
    
    if not openai_api_key:
        st.info("Please add your OpenAI API key in this tab to continue.", icon="🗝️")
    else:
        st.success("API Key received! Move to the Chat tab.")

with tab2:
    if not openai_api_key:
        st.warning("Please enter your API Key in the Settings tab first.")
    else:
        # Create an OpenAI client.
        client = OpenAI(api_key=openai_api_key)

        # Session state for messages
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("What is up?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Generate and stream response
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
