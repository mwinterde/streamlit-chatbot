import openai
import streamlit as st

from utils import (
    HIDE_MENU_STYLE,
    assistant_message,
    get_completion_from_chat_history,
    user_message,
)


def new_chat_input_submit():
    """
    Appends message to chat history and clears the text input box.
    """
    message = {"role": "user", "content": st.session_state.user_input}
    st.session_state.chat_history.append(message)
    st.session_state.user_input = ""


def delete_chat_history_submit():
    """
    Deletes chat history from session state and thus triggers start of a
    new conversation.
    """
    del st.session_state.chat_history


# Set page config
st.set_page_config(page_title="streamlit-chatbot", layout="wide")
st.markdown(HIDE_MENU_STYLE, unsafe_allow_html=True)

# Configure sidebar
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.05)
    openai.api_key = st.text_input("API key", type="password", key="api_key")
    st.write(
        "Get an API key from "
        "https://beta.openai.com/docs/developer-quickstart/your-api-keys"
    )

# Only show main app if API key is set
if not openai.api_key:
    st.warning("Please enter your OpenAI API key in the sidebar")
    st.stop()

# Initialize chat history if it doesn't exist yet
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display chat history
i = 0
last_message_from = "system"
for message in st.session_state.chat_history:
    if message["role"] == "user":
        user_message(message["content"], i)
    else:
        assistant_message(message["content"], i)
    i += 1
    last_message_from = message["role"]

# Generate assistant response if last message was from user
if last_message_from != "assistant":
    assistant_response = get_completion_from_chat_history(
        st.session_state.chat_history, temperature=temperature
    )
    assistant_message(assistant_response, i)
    # Append assistant response to chat history
    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

# Allow user to input new message
user_input = st.text_input(
    "Message", key="user_input", on_change=new_chat_input_submit
)

# Add empty space between input box and delete button
st.write("#")

# Allow user to delete chat history and thus start a new conversation
st.button("Delete chat history", on_click=delete_chat_history_submit)
