# Research question 2.

# Which programming languages do developers ask ChatGPT for
# help with, and how does this pattern change over time?

import os
import json
import pandas as pd
from glob import glob 

CURRENT_DIRECTORY = os.getcwd()
RAW_DATASETS_FILE_PATTERN = "/src/raw_datasets/*/*_"
DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
]
OUTPUT_FOLDER_PATH = "/src/filtered_datasets/rq2/"


def read_datasets(filepath):
    print(f"\tReading File: {filepath}")
    with open(filepath) as file_content:
        json_data = json.load(file_content)
        df = pd.json_normalize(json_data, record_path="Sources")
    return df[["RepoLanguage", "ChatgptSharing"]]


def process_data(category_dfs):
    print(f"\n\tProcessing category data...")
    df = pd.concat(category_dfs)
    chatgpt_sharing = pd.json_normalize(df["ChatgptSharing"].map(lambda x: x[0]))
    conversation_date = pd.to_datetime(chatgpt_sharing["DateOfConversation"], errors="coerce").dt.strftime("%m-%d-%Y")
    processed_df = df.drop("ChatgptSharing", axis=1).join(conversation_date)

    return processed_df[(processed_df.RepoLanguage.notnull()) & (processed_df.DateOfConversation.notnull())]


def write_processed_df(df, file):
    df.to_json(f"{CURRENT_DIRECTORY}{OUTPUT_FOLDER_PATH}{file.lower().replace(' ', '_')}.json", orient="records")
    df.to_csv(f"{CURRENT_DIRECTORY}{OUTPUT_FOLDER_PATH}{file.lower().replace(' ', '_')}.csv", index=False)


def prepare_datasets():
    for file in DATASET_CATEGORIES:
        print(f"\nPreparing category: {file}")
        filepaths = glob(f"{CURRENT_DIRECTORY}{RAW_DATASETS_FILE_PATTERN}{file.lower().replace(' ','_')}.json")
        category_dfs = [read_datasets(filepath) for filepath in filepaths]            
        processed_df = process_data(category_dfs)
        write_processed_df(processed_df, file)
        print(f"\tProcessed data exported.")

        del category_dfs
        del processed_df


def main():
    prepare_datasets()


main()
