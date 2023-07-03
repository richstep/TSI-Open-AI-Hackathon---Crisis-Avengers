# code/prep_items.py
import json
import re
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

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


    def prep_news_article(self, news_article):
        def remove_punctuation_except(text, allowed_chars=('.','')):
            cleaned_text = ''.join(c for c in text if c not in string.punctuation or c in allowed_chars)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            return cleaned_text

        transcript = remove_punctuation_except(news_article, allowed_chars=('.',''))
        transcript = transcript.lower()

        stop_words = set(stopwords.words('english'))
        word_tokens = word_tokenize(transcript)
        filtered_text = [word for word in word_tokens if not word in stop_words]
        transcript = ' '.join(filtered_text)

        transcript = re.sub(r'\s+', ' ', transcript).strip()
        transcript = re.sub(r"\s*\.\s*", ". ", transcript)
        transcript = re.sub(r",{2,}", ",", transcript)

        sep_token=" \n "
        transcript = transcript.replace(sep_token, " ")

        transcript = ' '.join(transcript.split())
        transcript = re.sub(r'\b(\w+)(\s+\1)+\b', r'\1', transcript, flags=re.IGNORECASE)

        return transcript