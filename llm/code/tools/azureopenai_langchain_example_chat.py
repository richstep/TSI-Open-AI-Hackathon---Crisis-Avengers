# llm/code/tools/azureopenai_langchain_example_chat.py
import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage


load_dotenv()

deployment_name = os.getenv("DEPLOYMENT_NAME_CHAT", "")
openai.api_type = os.getenv("API_TYPE", "")
openai.api_base = os.getenv("API_BASE", "")
openai.api_version = os.getenv("API_VERSION", "")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

BASE_URL = os.getenv("API_BASE", "")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
DEPLOYMENT_NAME = deployment_name
model = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version="2023-03-15-preview",
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
) # type: ignore



response = model(
  [
    HumanMessage(
      content="Translate this sentence from English to French. I love programming."
    )
  ]
)

print(response)

