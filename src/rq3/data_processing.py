# Research question 3.

# While interacting with ChatGPT, what emotions do developers generally display?

import json
import os
import re
from glob import glob
import pandas as pd


CURRENT_DIRECTORY = os.getcwd()
RAW_DATASETS_FILE_PATTERN = "/src/raw_datasets/*/*_"
DATASET_CATEGORIES = [
   "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
    "HN Sharings"
]
OUTPUT_FOLDER_PATH = "/src/rq3/processed_datasets/"

def extract_prompts(json_data):
    return [
        conversation["Prompt"]
        for source in json_data.get("Sources", [])
        if source.get("ChatgptSharing", []) and all(sharing['Status'] != 400 
            for sharing in source["ChatgptSharing"])
        for conversation in source.get("ChatgptSharing")[0].get("Conversations", [])
        if (prompt := conversation.get("Prompt"))
    ]

# Function to remove Unicode characters from each string in the array
def remove_unicode(input_array):
    cleaned_array = [string.encode('ascii', 'ignore').decode('ascii') for string in input_array]
    return cleaned_array


def write_to_file(data, output_file):
    file_location = CURRENT_DIRECTORY + OUTPUT_FOLDER_PATH + output_file.lower().replace(' ','_') + ".json"
    with open(file_location, "w") as outfile:
        json.dump(data,outfile, indent=2)

def process_data(raw_file_path):
    final_cleaned_prompt=[]
    for file_name in raw_file_path:
        print(f"\tReading File: {file_name}")
        with open(file_name) as file_content:
            json_data = json.load(file_content)
        
            #function call to get prompts from conversations
            prompts = extract_prompts(json_data)

            #remove html code from the prompt
            html_tag_pattern = re.compile (r'<.*?>')
            cleaned_prompt = [re.sub(html_tag_pattern,'',s) for s in prompts]

            #remove all unicodes such as in string "Continue, with Rebecca\u00e2\u0080\u0099s response"
            cleaned_prompt = remove_unicode(cleaned_prompt)

            #remove \n,(,)
            cleaned_prompt = [s.replace("\n", "").replace("(", "").replace(")", "") for s in cleaned_prompt]

            #remove extra space
            cleaned_prompt = [' '.join(s.split()) for s in cleaned_prompt]

            # Remove empty strings using list comprehension
            cleaned_prompt = [string for string in cleaned_prompt if string != ""]

            #Remove array if its length is less than 5
            cleaned_prompt = [s for s in cleaned_prompt if len(s) >= 5]
            final_cleaned_prompt.extend(cleaned_prompt)

    return final_cleaned_prompt  



def main():
    for file in DATASET_CATEGORIES:
        print(f"\nPreparing category: {file}")
        filepaths = glob(f"{CURRENT_DIRECTORY}{RAW_DATASETS_FILE_PATTERN}{file.lower().replace(' ','_')}.json")
        processed_data=process_data(filepaths) 
        write_to_file(processed_data, file)

