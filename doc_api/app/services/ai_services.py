import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API"),
    model="xiaomi/mimo-v2-flash:free",
    temperature=0.2,
    max_completion_tokens=10000,  
)
