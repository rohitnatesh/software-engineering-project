# Research question 2.

# Which programming languages do developers ask ChatGPT for
# help with, and how does this pattern change over time?

import os
import json
import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

CURRENT_DIRECTORY = os.getcwd()
RAW_DATASETS_FILE_PATTERN = "/src/raw_datasets/*/*_"
DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
]
FILTERED_DATA_FOLDER_PATH = "/src/rq2/processed_datasets/"


def read_datasets(filepath):
    print(f"\tReading File: {filepath}")
    with open(filepath) as file_content:
        json_data = json.load(file_content)
        df = pd.json_normalize(json_data, record_path="Sources")
    return df[["RepoLanguage", "ChatgptSharing"]]


def process_data(category_dfs):
    print("\n\tProcessing category data...")
    df = pd.concat(category_dfs)
    chatgpt_sharing = pd.json_normalize(df["ChatgptSharing"].map(lambda x: x[0]))
    conversation_date = pd.to_datetime(
        chatgpt_sharing["DateOfConversation"], errors="coerce"
    ).dt.strftime("%m-%d-%Y")
    processed_df = df.drop("ChatgptSharing", axis=1).join(conversation_date)

    return processed_df[
        (processed_df.RepoLanguage.notnull())
        & (processed_df.DateOfConversation.notnull())
    ]


def prepare_datasets():
    for file in DATASET_CATEGORIES:
        print(f"\nPreparing category: {file}")
        filepaths = glob(
            f"{CURRENT_DIRECTORY}{RAW_DATASETS_FILE_PATTERN}{file.lower().replace(' ','_')}.json"
        )
        category_dfs = [read_datasets(filepath) for filepath in filepaths]
        processed_df = process_data(category_dfs)

        processed_df.to_csv(
            f"{CURRENT_DIRECTORY}{FILTERED_DATA_FOLDER_PATH}{file.lower().replace(' ', '_')}.csv",
            index=False,
        )

        del category_dfs
        del processed_df
    print("\tProcessed data exported.")


def analyze_data():
    datasets = {}

    for category in DATASET_CATEGORIES:
        file_path = f"{CURRENT_DIRECTORY}{FILTERED_DATA_FOLDER_PATH}{category.lower().replace(' ', '_')}.csv"
        df = pd.read_csv(file_path, header=0)
        datasets[category] = df

    plt.rcParams.update({"figure.autolayout": True})

    for df_key in datasets:
        plt.figure(figsize=(10, 6))
        df = datasets[df_key]
        df["DateOfConversation"] = pd.to_datetime(df["DateOfConversation"])

        top_languages = df["RepoLanguage"].value_counts().nlargest(5).index

        plt.title(f"Top 5 Programming Languages Over Time: {df_key}")
        plt.xlabel("DateOfConversation")
        plt.ylabel("Count")

        for language in top_languages:
            language_data = df[df["RepoLanguage"] == language]
            language_counts = (
                language_data.groupby(pd.Grouper(key="DateOfConversation", freq="W"))
                .size()
                .reset_index(name="Count")
            )

            sns.scatterplot(
                x=language_counts["DateOfConversation"],
                y=language_counts["Count"],
                label=language,
                s=15,
            )

            window_size = 5
            rolling_average = (
                language_counts["Count"]
                .rolling(window=window_size, min_periods=1)
                .mean()
            )

            x = np.arange(len(language_counts["DateOfConversation"]))
            coeffs = np.polyfit(x, rolling_average, 1)
            trend = np.poly1d(coeffs)
            plt.plot(language_counts["DateOfConversation"], trend(x), linestyle="--")

        plt.legend(loc="upper left", bbox_to_anchor=(1, 1))
        plt.xticks(rotation=45)
        plt.tight_layout()

    plt.show()


def main():
    while True:
        choice = input(
            "\n1. Data Processing\n2. Data Analysis\n3. Exit\nEnter choice: "
        )

        if choice == "1":
            prepare_datasets()
        elif choice == "2":
            analyze_data()
        else:
            break


main()
