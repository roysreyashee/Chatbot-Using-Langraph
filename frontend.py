# Import Streamlit to build the chatbot UI.
import streamlit as st

# Import the custom chatbot backend and HumanMessage for sending user input.
from backend import chatbot
from langchain_core.messages import HumanMessage

# Configuration for the LangGraph chat session.
# The thread_id helps maintain a persistent conversation state for the same chat.
CONFIG = {'configurable': {'thread_id': 'thread_1'}}

# Initialize the chat history in the session state if it does not already exist.
# This keeps the conversation across reruns in the Streamlit app.
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Render the stored conversation history when the app loads or reruns.
# Each message is displayed in the appropriate chat bubble (user or assistant).
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

# Example chat messages kept as comments for quick testing during development.
# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('assistant'):
#     st.text('How can I help you?')

# with st.chat_message('user'):
#     st.text('My name is Sreyashee')

# Create an input box at the bottom of the chat interface.
# This waits for the user to type a message and press Enter.
user_input = st.chat_input('Type Here...')

# If the user has entered a message, process it and generate a response.
if user_input:
    # Save the user's message in the conversation history before generating a reply.
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})

    # Display the user's message in the chat UI.
    with st.chat_message('user'):
        st.text(user_input)

    # Send the user message to the chatbot backend with the configured thread.
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)

    # Extract the AI response from the last message in the backend response.
    # The [1] index is used because the response structure contains multiple content parts.
    ai_message = response['messages'][-1].content

    # Alternative approach to extract text from a structured content list:
    # ai_message = "\n".join(
    #     block['text']
    #     for block in content
    #     if isinstance(block, dict) and block.get('type') == 'text'
    # )

    # Save the assistant's reply in the conversation history.
    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})

    # Display the assistant's response in the chat UI.
    with st.chat_message('assistant'):
        st.text(ai_message)