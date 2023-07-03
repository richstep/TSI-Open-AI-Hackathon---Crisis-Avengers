#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_type = os.getenv("API_TYPE", "")
openai.api_base = os.getenv("API_BASE", "")
openai.api_version = os.getenv("API_VERSION", "")
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")

joke = "Tell me a joke about a spiderman movie"

response = openai.ChatCompletion.create(
  engine="gpt-35-turbo-16k",
  messages=[{"role": "user", "content": joke}],
  temperature=0.7,
  max_tokens=800,
  top_p=0.95,
  frequency_penalty=0,
  presence_penalty=0,
  stop=None)

print(response)