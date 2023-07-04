# project/code/tsi_hackathon.py

import json
import time
import openai
import os
from data_preperation import DataProcessor
from openai_apicall import OpenAIApiCall
from azure_openai_apicall import AzureOpenAIApiCall
from azure_openai_apicall_chat import AzureOpenAIApiCall_Chat
from dotenv import load_dotenv

load_dotenv()

# set the files
data_file = os.getenv("DATA_FILE", "")
ids_to_skip_file = os.getenv("IDS_TO_SKIP_FILE", "")
results_file = os.getenv("RESULTS_FILE", "")

# create a data processor instance and prepare the items
data_processor = DataProcessor(data_file, ids_to_skip_file)
prepped_items = data_processor.prep_items()

# create an instance of the ApiCall class
api_call = AzureOpenAIApiCall_Chat()

# print the results
print("Matching items:")
for item in prepped_items:
    print(f"- {item['ID']}:  ({item['Text'][:50]})")

results = []
ids_to_skip = []
for idx, item in enumerate(prepped_items, 1):
    print(f"Processing item {idx} of {len(prepped_items)} for id {item['ID']}")

    try:
        # *** call API ****
        openai_result = api_call.run(text=item["Text"])
        data_dict = json.loads(openai_result.content)

        # Add new key-value pair
        data_dict['ID'] = item["ID"]

        # Assign each item to a variable
        summary = data_dict.get('summary')
        crisis_assessment = data_dict.get('crisis_assessment')
        crisis_ranking = data_dict.get('crisis_ranking')
        locations_affected = data_dict.get('locations_affected')
        people_affected = data_dict.get('people_affected')

        # check if people_affected is a dictionary
        if isinstance(people_affected, dict):
            specific_count = people_affected.get('specific_count')
            by_location = people_affected.get('by_location')
            estimate = people_affected.get('estimate')

        # write the ID value to the ids_to_skip if it's not a humanitarian crisis
        if isinstance(crisis_ranking, int) and crisis_ranking < 2:
            ids_to_skip.append(str(item["ID"]))

        results.append(data_dict)

    except openai.OpenAIError as e:
        if e.code == "content_filter":
            print(f"- {item['ID']}: Content filter error")
            json_result = {"ID": item["ID"], "json_result": str(e)}
            ids_to_skip.append(str(item["ID"]))
            results.append(json_result)
        else:
            print("Error: " + str(e))
        continue
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        continue

    time.sleep(2) # optional delay to avoid rate limiting

# write to the files
with open(ids_to_skip_file, 'a') as skip_output_file:
    for id in ids_to_skip:
        skip_output_file.write(id + '\n')

with open(results_file, 'a') as result_output_file:
    for result in results:
        result_output_file.write(json.dumps(result) + '\n')
