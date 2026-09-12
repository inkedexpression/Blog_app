from langgraph.graph import StateGraph , START ,END
from dotenv import load_dotenv
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from typing import TypedDict
import os 

os.environ['LANGCHAIN_PROJECT'] = 'Langraph2'

load_dotenv()

model = ChatNVIDIA(model='nvidia/nemotron-3-super-120b-a12b')

class ChatState(TypedDict):

    message : list[str]


def chatbot(state):

    message = state['message']
    response = model.invoke(message).content

    return {'message':response}

graph = StateGraph(ChatState)

graph.add_node('chatbot',chatbot)

graph.add_edge(START,'chatbot')
graph.add_edge('chatbot',END)

workflow = graph.compile()


inital_state = {'message':'what is the capital of russia'}

result = workflow.invoke(inital_state)

print(result['message'])