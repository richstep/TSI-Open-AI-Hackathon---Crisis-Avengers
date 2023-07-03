# project/code/tsi_hackathon.py

import json
import time
import openai
from data_preperation import DataProcessor
from openai_apicall import OpenAIApiCall
from azure_openai_apicall import AzureOpenAIApiCall
from azure_openai_apicall_chat import AzureOpenAIApiCall_Chat

# define the files
data_file = 'llm/files/eventsdata_sample_text_5k.json'
ids_to_skip_file = 'llm/files/ids_to_skip.txt'
results_file = 'llm/files/results.json'

# define the keywords
keywords = {'mississippi', 'hawaii50'}

# create a data processor instance and prepare the items
data_processor = DataProcessor(data_file, ids_to_skip_file)
prepped_items = data_processor.prep_items()

# create a single instance of the ApiCall class
#api_call = OpenAIApiCall()
#api_call = AzureOpenAIApiCall()
api_call = AzureOpenAIApiCall_Chat()

# print the results
print("Matching items:")
for item in prepped_items:
    print(f"- {item['_c0']}:  ({item['Text'][:25]})")

with open(ids_to_skip_file, 'a') as skip_output_file, open(results_file, 'a') as result_output_file:
    ii = 0
    for item in prepped_items:
        ii += 1
        print(f"Processing item {ii} of {len(prepped_items)} for id {item['_c0']}")
        #if ii == 10:
        #    break

        try:
            # *** call API ****
            openai_result = api_call.run(text=item["Text"])
            #openai_result = api_call.run(text=item["Text"])
            print(openai_result)
            print(type(openai_result))
            import json

            # Extract content from openai_result
            json_string = openai_result.content

            # Parse JSON string into a Python dictionary
            data_dict = json.loads(json_string)

            # Add new key-value pair
            data_dict['_c0'] = item["_c0"]

            # Convert dictionary back to JSON string with new entry
            json_string_with_new_entry = json.dumps(data_dict)

            # Now you can parse this new JSON string back into a dictionary and assign items to variables
            new_data_dict = json.loads(json_string_with_new_entry)

            # Assign each item to a variable
            summary = new_data_dict['summary']
            crisis_assessment = new_data_dict['crisis_assessment']
            crisis_ranking = new_data_dict['crisis_ranking']
            locations_affected = new_data_dict['locations_affected']
            people_affected = new_data_dict['people_affected']

            # to access nested items
            specific_count = people_affected.get('specific_count', None)
            by_location = people_affected.get('by_location', None)
            estimate = people_affected.get('estimate', None)

            # write the _c0 value to the ids_to_skip_file if it's not a humanitarian crisis
            if crisis_ranking < 2:
                skip_output_file.write(str(item["_c0"]) + '\n')

            result_output_file.write(json.dumps(new_data_dict) + '\n')
                
        # write the openai_result to the result_file
        except openai.OpenAIError as e:
            if e.code == "content_filter":
                print(f"- {item['_c0']}: Content filter error")
                json_result = {"_c0": item["_c0"], "json_result": str(e)}
                skip_output_file.write(str(item["_c0"]) + '\n')
                result_output_file.write(json.dumps(json_result) + '\n')
            else:
                print("Error: " + str(e))
            continue

        time.sleep(2) # optional delay to avoid rate limiting
