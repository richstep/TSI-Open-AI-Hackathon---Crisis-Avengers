# code/azure_openai_apicall_chat.py

import json
import os
import openai
import backoff
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import List, Dict

load_dotenv()

class AzureOpenAIApiCall_Chat:
    def __init__(self, temperature=0):
        self.temperature = temperature
        self.deployment_name = os.getenv("DEPLOYMENT_NAME_CHAT", "")
        self.BASE_URL = os.getenv("API_BASE", "")
        self.API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

    def run(self, text):
        prompt_text = text

        response = call_openai(prompt_text, self.deployment_name, self.BASE_URL, self.API_KEY)


        return response


def call_openai(news_article, deployment_name, base_url, api_key):



    model = AzureChatOpenAI(
        openai_api_base=base_url,
        openai_api_version="2023-03-15-preview",
        deployment_name=deployment_name,
        openai_api_key=api_key,
        openai_api_type="azure",
    ) # type: ignore

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

    # news_query = '''

    # ###
    # News Article:

    # Two monkeys taken from the Dallas Zoo were found Tuesday in an abandoned home after going missing the day before from their enclosure, which had been cut. But no arrests have been made, deepening the mystery at the zoo that has included other cut fences, the escape of a small leopard and the suspicious death of an endangered vulture.
    # '''

    _input = prompt.format_prompt(query=news_article)

    response = model(
    [
        HumanMessage(
        content=_input.to_string()
        )
    ]
    )
    
    return response