from langchain_ollama import ChatOllama

model = ChatOllama(model="qwen2.5:3B")

def get_response(messages):
    response = model.stream(messages)

    return response