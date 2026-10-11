import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread_1'}}

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

#loading the convo history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])
# with st.chat_message('user'):
#     st.text('Hi')

# with st.chat_message('assistant'):
#     st.text('How can I help you?')

# with st.chat_message('user'):
#     st.text('My name is Sreyashee')

user_input = st.chat_input('Type Here...')

if user_input:
    #first add the message to message_history 
    st.session_state['message_history'].append({'role': 'user' , 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG)
    # ai_message = response['messages'][-1].content[1]

#     ai_message = "\n".join(
#     block['text']
#     for block in content
#     if isinstance(block, dict) and block.get('type') == 'text'
# )
    #adding ai message to message_history
    
    with st.chat_message('assistant'):
       ai_message = st.write_stream(
         message_chunk.content for message_chunk, metadata in chatbot.stream(
               {'messages': [HumanMessage(content=user_input)]},
                config={'configurable': {'thread_id': 'thread_1'}},
                stream_mode="messages"
           )
       )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})