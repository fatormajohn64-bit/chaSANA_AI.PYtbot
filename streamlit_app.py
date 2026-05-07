import streamlit as st
from openai import OpenAI

# 1. Setup Page Configuration
st.set_page_config(page_title="AI Chatbot", layout="wide")

st.title("💬 Chatbot")

# 2. Create Tabs
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
