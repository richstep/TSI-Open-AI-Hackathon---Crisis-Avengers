# code/tools/azureopenai_example.py
import os
import openai
from langchain.llms import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

deployment_name = os.getenv("DEPLOYMENT_NAME", "")
# os.environ["OPENAI_API_TYPE"] = os.getenv("API_TYPE", "")
# os.environ["OPENAI_API_BASE"] = os.getenv("API_BASE", "")
# os.environ["OPENAI_API_VERSION"] = os.getenv("API_VERSION", "")
os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")

print(deployment_name)
#print(os.environ["OPENAI_API_TYPE"])
#print(os.environ["API_BASE"])
#print(os.environ["API_VERSION"])
print(os.environ["OPENAI_API_KEY"])

openai.api_type = os.getenv("API_TYPE", "")
openai.api_base = os.getenv("API_BASE", "")
openai.api_version = os.getenv("API_VERSION", "")
#openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

print(openai.api_type)
print(openai.api_base)
print(openai.api_version)
print(openai.api_key)


# response = openai.Completion.create(
#     engine="text-davinci-002-prod",
#     prompt="This is a test",
#     max_tokens=5
# )

prompt = "tell me a joke about a spiderman cartoon movie"

llm = AzureOpenAI(
        deployment_name=deployment_name,
        model_name="text-davinci-003",
        client=None)

response = llm(prompt)

print(response)