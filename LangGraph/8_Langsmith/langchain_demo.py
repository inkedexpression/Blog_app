from langchain_nvidia_ai_endpoints import ChatNVIDIA
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

model = ChatNVIDIA(model='nvidia/nemotron-3-super-120b-a12b')

prompt = PromptTemplate.from_template("{question}")

chain = prompt | model | StrOutputParser()

response = chain.invoke({'question':'what is the capital of japan'})
print(response)