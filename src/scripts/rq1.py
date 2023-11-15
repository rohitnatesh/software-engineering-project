# Research question 1.

# Do developers tend to exhibit a deviation from their initial
# topic of inquiry as the conversation unfolds with ChatGPT?

import os
import json
from glob import glob

CURRENT_DIRECTORY = os.getcwd()
RAW_DATASETS_FILE_PATTERN = "/src/raw_datasets/*/*_"
DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings"
]

OUTPUT_FOLDER_PATH = "/src/filtered_datasets/rq1/"

def read_json_data(filepath):
    print(f"\tReading File: {filepath}")
    with open(filepath) as f:
        data = json.load(f)
    return data

def preprocess_data(data):
    processed_data = {}

    processed_data["ChatgptConversations"] = []

    for file_data in data:

        for instance in file_data["Sources"]:

            # ID = instance["Sha"]
            Interactions = {}

            for sharing in instance["ChatgptSharing"]:
                if sharing["Status"] == 404:
                    break

                if sharing["NumberOfPrompts"] >= 2:            
                    Prompts_list = []
                    Answers_list = []

                    for response in sharing["Conversations"]:
                        Prompts_list.append(response["Prompt"])
                        Answers_list.append(response["Answer"])
                    Interactions["Prompts"] = Prompts_list
                    Interactions["Answers"] = Answers_list  

                    processed_data["ChatgptConversations"].append(Interactions)

    return processed_data


def write_data(data,file):
    file_loc = CURRENT_DIRECTORY + OUTPUT_FOLDER_PATH + file.lower().replace(' ','_') + ".json"
    print(file_loc)
    with open(file_loc,"w") as outfile:
        json.dump(data, outfile)    

def main():
    for file in DATASET_CATEGORIES:
        filepaths = glob(f"{CURRENT_DIRECTORY}{RAW_DATASETS_FILE_PATTERN}{file.lower().replace(' ','_')}.json")
        print(filepaths)
        data = [read_json_data(filepath) for filepath in filepaths]
        processed_data = preprocess_data(data)
        write_data(processed_data,file)

main()