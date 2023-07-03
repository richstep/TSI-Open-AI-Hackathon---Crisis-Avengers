# llm/code/tools/azureopenai_langchain_example_chat.py
import os
import openai
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from typing import List, Dict
from pydantic import BaseModel, Field

load_dotenv()

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME_CHAT", "")
BASE_URL = os.getenv("API_BASE", "")
API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

model = AzureChatOpenAI(
    openai_api_base=BASE_URL,
    openai_api_version="2023-03-15-preview",
    deployment_name=DEPLOYMENT_NAME,
    openai_api_key=API_KEY,
    openai_api_type="azure",
) # type: ignore


content_string = """
As an expert evaluator, I need you to assess whether a given news article indicates a potential humanitarian crisis. Please read the article and provide your judgment based on the content, considering factors such as the magnitude of humanitarian impact.
The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": {"type": "string"}}}, "required": ["foo"]}
the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

Here is the output schema:
"""

json_schema_string = r'''{
"properties": {
"summary": {"title": "Summary", "description": "Brief summary of the news article", "type": "string"}, 
"crisis_assessment": {"title": "Crisis Assessment", "description": "Your judgement about the crisis potential", "type": "string"}, 
"crisis_ranking": {"title": "Crisis Ranking", "description": "Rank the crisis on a scale of 1(low) to 10(high)", "type": "integer"}, 
"locations_affected": {"title": "Locations Affected", "description": "Location names", "type": "array", "items": {"type": "string"}}, 
"people_affected": {"title": "People Affected", "description": "Location names", "type": "array", "items": {"type": "string"}}, 
"crisis_category": {"title": "Crisis Category", "description": "Identified crisis", "type": "string"}, 
"key_stakeholders": {"title": "Key Stakeholders", "description": "List of key involved parties", "type": "string"}, 
"causes_and_triggers": {"title": "Causes And Triggers", "description": "Causes or triggers of the crisis", "type": "string"}, 
"response_efforts": {"title": "Response Efforts", "description": "Efforts in response to the crisis", "type": "string"}, 
"timeline_and_progress": {"title": "Timeline And Progress", "description": "Description of the crisis timeline and progress", "type": "string"}, 
"resource_requirements": {"title": "Resource Requirements", "description": "Required resources to manage the crisis", "type": "string"}}, 
"required": ["summary", "crisis_assessment", "crisis_ranking", "locations_affected", "people_affected", "crisis_category", "key_stakeholders", "causes_and_triggers", "response_efforts", "timeline_and_progress", "resource_requirements"]
}'''

news_arctile = '''two monkeys taken dallas zoo found tuesday abandoned home going missing day enclosure cut. arrests made deepening mystery zoo included cut fences escape small leopard suspicious death endangered vulture. dallas police said found two emperor tamarin monkeys getting tip could abandoned home lancaster located south zoo. animals located safe closet returned zoo veterinary evaluation. police said earlier tuesday still working determine whether incidents last weeks related. meanwhile louisiana officials investigating 12 squirrel monkeys taken zoo sunday considering whether could connection. heres known far incidents happened dallas zoo closed jan. 13 workers arriving morning found clouded leopard named nova missing. search included police leopard weighing 2025 pounds 911 kilograms found later day near habitat. police said cutting tool intentionally used make opening enclosure. similar gash also found enclosure langur monkeys though none got appeared harmed police said. jan. 21 endangered lappetfaced vulture named pin found dead arriving workers. gregg hudson zoos president ceo called death “ suspicious ” said vulture “ wound declined give details. hudson said news conference following pins death vulture enclosure didnt appear tampered. monday police said two emperor tamarin monkeys — long whiskers look like mustache — believed taken someone cut opening enclosure. following day police released photo video man said wanted talk monkeys. photo shows man eating doritos chips walking video clip seen walking path. could motive taking monkeys lynn cuny founder president wildlife rescue rehabilitation kendalia texas said ’ surprised turns monkeys taken sold. depending buyer said monkey like could sold “ several thousands ” dollars. “ primates highdollar animals wildlife pet trade country ” cuny said. “ everybody wants one wants one wrong reasons — ’ never good reason wild animal pet. ” said variety ways taken monkeys could danger improper diet exposure cold. temperatures dallas dipped 20s tuesday winter storm. known vulture pins death hard staff zoo official said. vulture “ beloved member bird department ” according harrison edell zoo ’ executive vice president animal care conservation. speaking news conference edell said pin least 35 years old zoo 33 years. “ lot teams worked closely time ” edell said. pin one four lappetfaced vultures zoo said sired 11 offspring first grandchild hatched early 2020. edell said pins death personal loss also loss species “ could potentially go extinct lifetime. ” known security hudson zoos ceo said news conference following pin ’ death normal operating procedures included 100 cameras monitor public staff exhibit areas number increased. overnight presence security staff also raised. possible said zoo officials limited ability animals go outside overnight. nova went missing officials said reviewed surveillance video showed. zoo closed tuesday wednesday due storm. happened louisiana 12 squirrel monkeys discovered missing sunday enclosure zoo states southeast. habitat zoosiana broussard 60 miles 96 kilometers west baton rouge “ compromised ” damage done get city police chief vance olivier said tuesday. declined provide details damage citing ongoing investigation. said police suspects yet still searching video files. zoosiana said facebook post remaining monkeys assessed appear unharmed. incidents dallas zoo 2004 340pound 154kilogram gorilla named jabari jumped wall went 40minute rampage injured three people police shot killed animal.'''

human_message = content_string + json_schema_string + news_arctile

# response = model(
#   [
#     HumanMessage(
#       content=human_message
#     )
#   ]
# )

 
### NOW LETS TRY USING TEMPLATE ###
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import (
    PromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
class Location(BaseModel):
    name: str = Field(description="Location name")
    category: str = Field(description="Location category such as country, state, region, city, or unknown")

class PeopleAffected(BaseModel):
    specific_count: int = Field(description="Total count of people affected")
    by_location: Dict[str, int] = Field(description="Count of people affected in each mentioned location")
    estimate: str = Field(description="Rough estimate if an exact count isn't provided")

class NewsCrisis(BaseModel):
    summary: str = Field(description="Brief summary of the news article")
    crisis_assessment: str = Field(description="Your judgement about the crisis potential")
    crisis_ranking: int = Field(description="Rank the crisis on a scale of 1(low) to 10(high)")
    locations_affected: List[Location] = Field(description="List of locations affected")
    people_affected: PeopleAffected = Field(description="Information about the people affected by the crisis")

parser = PydanticOutputParser(pydantic_object=NewsCrisis)

prompt = PromptTemplate(
    template="As an expert evaluator, I need you to assess whether a given news article indicates a potential humanitarian crisis. Please read the article and provide your judgment based on the content, considering factors such as the magnitude of humanitarian impact.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

news_query = '''

###
News Article:

Two monkeys taken from the Dallas Zoo were found Tuesday in an abandoned home after going missing the day before from their enclosure, which had been cut. But no arrests have been made, deepening the mystery at the zoo that has included other cut fences, the escape of a small leopard and the suspicious death of an endangered vulture.
'''

_input = prompt.format_prompt(query=news_query)

response = model(
  [
    HumanMessage(
      content=_input.to_string()
    )
  ]
)
print(response)

