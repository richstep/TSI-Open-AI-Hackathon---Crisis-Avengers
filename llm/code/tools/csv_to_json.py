import csv
import json
import os

 
# Function to convert a CSV to JSON
# Takes the file paths as arguments
def make_json(csvFilePath, jsonFilePath):
     
    # create a dictionary
    data = {}
     

    # Open a csv reader called DictReader
    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)

        # Convert each row into a dictionary
        # and add it to data
        skipped_rows = 0
        read_rows = 0
        for row in csvReader:
            read_rows += 1
            # Assuming a column named 'ID' to
            # be the primary key
            key = row['ID']

            # Check if the key is an integer
            if not key.isdigit():
                skipped_rows += 1
                continue

            if row["V2Themes"] is not None:
                row["V2Themes"] = [theme.strip() for theme in row["V2Themes"].split(";")]

                locations = []
                seen_locations = set()  # Track seen location names to avoid duplicates

                for loc in row["V2Locations"].split(";"):
                    split_loc = loc.split("#")
                    location_dict = {
                        "LocationName": split_loc[1],
                        "LocationCountryCode": split_loc[2],
                        "LocationPopulation": split_loc[4],
                        "LocationLatitude": split_loc[5],
                        "LocationLongitude": split_loc[6]
                    }

                    # Check if location name is already seen
                    if location_dict["LocationName"] not in seen_locations:
                        locations.append(location_dict)
                        seen_locations.add(location_dict["LocationName"])

                row["V2Locations"] = locations

            data[key] = row

        print(f"Red {read_rows} rows")
        print(f"Skipped {skipped_rows} rows")
 
    # Open a json writer, and use the json.dumps()
    # function to dump data
    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(data, indent=4))

# print workinig directoroy         
print(f"Working directory: {os.getcwd()}") 
 
# Decide the two file paths according to your
# computer system
csvFilePath = r'llm/files/eventsdata_sample_text_5k_juneorjuly.csv'
jsonFilePath = r'llm/files/eventsdata_sample_text_5k_juneorjuly.json'

# Call the make_json function
make_json(csvFilePath, jsonFilePath)