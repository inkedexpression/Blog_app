from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv

load_dotenv()

model = ChatNVIDIA(model='meta/muse-glimmer-30b')

result = model.invoke("hi")
print(result.content)