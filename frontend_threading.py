# Import Streamlit to build the chatbot UI.
import streamlit as st

# Import the custom chatbot backend and HumanMessage for sending user input.
from backend import chatbot
from langchain_core.messages import HumanMessage
import uuid

#########################################Utility Functions###########################################
#generating dynamic thread_id
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)

##################################Session Setup##################################
# Initialize the chat history in the session state if it does not already exist.
# This keeps the conversation across reruns in the Streamlit app.
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

#if the thread_id is not present in the  session_state then generate thread_id
if 'thread_id' not in st.session_state:
    st.session_state['thread_id']= generate_thread_id()


#to show the ongoing chat threads in the sidebar
if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads']=[]

add_thread(st.session_state['thread_id'])

# Configuration for the LangGraph chat session.
# The thread_id helps maintain a persistent conversation state for the same chat.
CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

##########################################SIDEBAR UI###########################################

st.sidebar.title('LangGraph Chatbot')

if st.sidebar.button('New Chat'):
    reset_chat()

st.sidebar.title('My Conversations')

for thread_id in st.session_state['chat_threads']:
    st.sidebar.button(str(thread_id))


#**************************** MAIN UI *******************************#
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

if user_input:
    # First add the message to chat history.
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    assistant_response = []

    def generate_response():
        for message_chunk, _ in chatbot.stream(
            {"messages": [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages",
        ):
            content = message_chunk.content

            # Some chunks contain plain strings.
            if isinstance(content, str):
                if content:
                    assistant_response.append(content)
                    yield content

            # Other chunks contain lists of content blocks.
            elif isinstance(content, list):
                for block in content:
                    if isinstance(block, dict) and block.get("type") == "text":
                        text = block.get("text", "")
                        if text:
                            assistant_response.append(text)
                            yield text

    with st.chat_message("assistant"):
        st.write_stream(generate_response())

    ai_message = "".join(assistant_response)

    # Save the complete assistant response to chat history.
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })
