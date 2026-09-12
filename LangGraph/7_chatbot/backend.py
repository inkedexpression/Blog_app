from langgraph.graph import StateGraph , START ,END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict , Annotated
from langchain_core.messages import BaseMessage , HumanMessage , SystemMessage
from dotenv import load_dotenv 
from langgraph.graph.message import add_messages
import sqlite3

from langgraph.prebuilt import ToolNode , tools_condition
from tools import get_stock_price , get_weather , search_tool , calculator

load_dotenv()
# ----------------------------------------------------------------------------------------------
# LLM models
# model = ChatNVIDIA(model='nvidia/nemotron-3-super-120b-a12b')
model = ChatNVIDIA(model='openai/gpt-oss-20b')
# model = ChatNVIDIA(model='google/gemma-4-31b-it')
# ----------------------------------------------------------------------------------------------

# LLM and tools
tools = [get_weather,get_stock_price,calculator,search_tool]
model_with_tools = model.bind_tools(tools)
# ----------------------------------------------------------------------------------------------

class ChatBotState(TypedDict):

    messages : Annotated[list[BaseMessage],add_messages]

# ----------------------------------------------------------------------------------------------
def ChatBot(state):
    message = state['messages']
    messages = [SystemMessage(content="""
You are a helpful assistant.
When a tool returns information:
- Use the tool result to answer the user's question.
- Do not blindly copy the raw tool output.
- Give a clean, concise answer.
- Preserve all numerical values exactly as returned by the tool.
- Do not invent information."""),*message]
    response = model_with_tools.invoke(messages)
    return {'messages':[response]}
# ----------------------------------------------------------------------------------------------
tool_node = ToolNode(tools) # executes tool calls
# ----------------------------------------------------------------------------------------------
conn = sqlite3.connect(database='chatbot.db',check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)
# ----------------------------------------------------------------------------------------------
graph = StateGraph(ChatBotState)

graph.add_node('ChatBot',ChatBot)
graph.add_node('tools',tool_node)

graph.add_edge(START,'ChatBot')
graph.add_conditional_edges('ChatBot',tools_condition)
graph.add_edge('tools','ChatBot')

chatbot = graph.compile(checkpointer=checkpointer)
# ----------------------------------------------------------------------------------------------
config={'configurable':{'thread_id':'thread-10'}}
response = chatbot.invoke({'messages':[HumanMessage(content="what is weather in mangalore")]},
               config=config)
# ----------------------------------------------------------------------------------------------


def reterive_threads():
    all_thread = set()
    for item in checkpointer.list(None):
        all_thread.add(item.config['configurable']['thread_id'])

    return list(all_thread)

# ----------------------------------------------------------------------------------------------
# testing 

# response = chatbot.invoke({"message":[HumanMessage(content="what is the weather in bangalore")]})

# print(response['messages'][-1].content)