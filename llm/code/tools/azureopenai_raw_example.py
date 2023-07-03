#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv("API_TYPE", "")
openai.api_base = os.getenv("API_BASE", "")
openai.api_version = os.getenv("API_VERSION", "")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

response = openai.Completion.create(
  engine="davinci",
  prompt="",
  temperature=1,
  max_tokens=100,
  top_p=0.5,
  frequency_penalty=0,
  presence_penalty=0,
  best_of=1,
  stop=None)

print(response)