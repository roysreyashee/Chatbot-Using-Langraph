from langgraph.graph import StateGraph , START , END, add_messages
from typing import TypedDict, Literal, Annotated 
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI  
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
load_dotenv()


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

checkpointer = MemorySaver()
graph = StateGraph(ChatState)

#adding nodes 
# Register the 'chat_node' function as a node in the graph
graph.add_node('chat_node', chat_node)

#adding edges
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

graph.compile(checkpointer=checkpointer)


chatbot = graph.compile(checkpointer=checkpointer)

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