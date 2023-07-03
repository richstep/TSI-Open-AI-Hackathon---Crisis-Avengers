# code/azure_openai_apicall.py
# code/azure_openai_apicall.py
import json
import os
import openai
import backoff
from langchain import PromptTemplate, LLMChain
from langchain.llms import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()




class AzureOpenAIApiCall:
    def __init__(self, temperature=0):
        self.temperature = temperature
        self.deployment_name = os.getenv("DEPLOYMENT_NAME", "")
        openai.api_type = os.getenv("API_TYPE", "")
        openai.api_base = os.getenv("API_BASE", "")
        openai.api_version = os.getenv("API_VERSION", "")
        os.environ["OPENAI_API_KEY"] = os.getenv("AZURE_OPENAI_API_KEY", "")

    def run(self, text):
        prompt_text = text

        response = call_openai(prompt_text, self.deployment_name)

        #result = response.choices[0].text.strip()
        #json_data = fix_json(result)

        return response


def call_openai(prompt, deployment_name):
    llm = AzureOpenAI(
        deployment_name=deployment_name,
        model_name="text-davinci-003",
        client=None)

    response = llm(prompt)

    return response

def fix_json(json_str):
    try:
        return json.loads(json_str)
    except ValueError as e:
        try:
            # Find the position of the first error in the string
            pos = e.args[1]
            # Attempt to fix the JSON string
            if json_str[pos-1] == ',':
                # Remove the trailing comma
                fixed_json = json_str[:pos-1] + json_str[pos:]
            else:
                # Add a missing closing brace or bracket
                brace = {'{': '}', '[': ']'}
                last_open = [i for i, c in enumerate(json_str[:pos]) if c in brace.keys()][-1]
                missing = brace[json_str[last_open]]
                fixed_json = json_str[:pos] + missing + json_str[pos:]
            # Retry with the fixed JSON string
        except IndexError:
            # If we can't find the position of the error, just return an empty json string
            return json_str
           
        return fix_json(fixed_json)