from langgraph.graph import StateGraph , START , END, add_messages
from typing import TypedDict, Literal, Annotated 
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI  
from langgraph.checkpoint.sqlite import SqliteSaver
from dotenv import load_dotenv
load_dotenv()
import sqlite3

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages] #add_m


llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite")
def chat_node(state: ChatState):
    #take user query from state 
    messages = state["messages"]
    #send to llm
    response = llm.invoke(messages)
    #store response in state 
    return {'messages': [response]}

# The checkpointer stores the graph state (messages, tool outputs, etc.) in a SQLite database.
# This allows LangGraph to persist conversation history across invocations and resume a thread
# from the last saved state using a configurable thread_id.
conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
graph = StateGraph(ChatState)

#adding nodes 
# Register the 'chat_node' function as a node in the graph
graph.add_node('chat_node', chat_node)

#adding edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

graph.compile(checkpointer=checkpointer)


chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    """Return all saved thread IDs stored in the SQLite checkpointer.

    Each checkpoint represents a persisted graph state for a specific thread.
    The config for each checkpoint contains a `thread_id`, which we collect and
    return as a unique list of active conversation threads.
    """
    # List every stored checkpoint from the SQLite-backed checkpointer.
    # Each checkpoint includes metadata under `config['configurable']`.
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        # Extract the thread ID from the checkpoint configuration and keep only
        # unique values so each thread appears once in the final result.
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)


# thread_id = '1'
# while True:

#     user_message = input('Type here: ')

#     print('User: ', user_message)

#     if user_message.strip().lower() in ['exit', 'bye', 'quit']:
#         break

#     config = {'configurable': {'thread_id': thread_id}}

#     # Send the user's latest message to the chatbot graph.
#     # The graph expects a state dictionary with a "messages" list,
#     # so we wrap the raw text in a HumanMessage before invoking the model.
#     response = chatbot.invoke({'messages': [HumanMessage(content=user_message)]}, config=config)

#     print('AI :', response['messages'][-1].content)

# chatbot.get_state(config=config)

#test
# CONFIG = {'configurable': {'thread_id':'thread-1'}}

# resp = chatbot.invoke(
#     {"messages": [HumanMessage(content='Hi , my name is Sreyashee')]},
#     config=CONFIG,
# )

# print(resp)


