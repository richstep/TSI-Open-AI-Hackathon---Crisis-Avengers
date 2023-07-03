# code/prep_items.py
import json
import re

class DataProcessor:
    def __init__(self, data_file, ids_to_skip_file):
        self.data_file = data_file
        self.ids_to_skip_file = ids_to_skip_file
        self.c0_set = set()
        self.c0_set_for_file = set()
        self.load_ids_to_skip()

    def load_ids_to_skip(self):
        try:
            with open(self.ids_to_skip_file, 'r') as file:
                self.c0_set_for_file = {line.strip() for line in file}
        except FileNotFoundError:
            pass

    def prep_items(self):
        # load json file
        with open(self.data_file) as f:
            data = json.load(f)

        results = []

        for item in data.values():
            _c0 = str(item["_c0"])
            if _c0 not in self.c0_set_for_file and _c0 not in self.c0_set and item["Text"] != "null" and item["Text"] is not None:
                # clean the text        
                text = re.sub(r"<[^>]+>", "", item["Text"])  # remove HTML tags
                text = re.sub(r"\s+", " ", text)  # remove extra spaces
                text = text.replace('\n', item["Text"])  # remove newlines
                text = text.strip()  # remove leading and trailing spaces

                # add the item to the results list
                results.append({"_c0": item["_c0"], "V2Themes": item["V2Themes"], "Text": text})
                self.c0_set.add(_c0)

        # remove _c0 items from results if the same _c0 value exists in c0_set_for_file
        results = [result for result in results if str(result["_c0"]) not in self.c0_set_for_file]
        return results
