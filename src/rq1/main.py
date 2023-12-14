# Research question 1.

# Do developers tend to exhibit a deviation from their initial
# topic of inquiry as the conversation unfolds with ChatGPT?

import os
import json
from glob import glob
from statistics import mean
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

CURRENT_DIRECTORY = os.getcwd()
RAW_DATASETS_FILE_PATTERN = "/src/raw_datasets/*/*_"
DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
    "HN Sharings"
]

OUTPUT_FOLDER_PATH = "/src/rq1/processed_datasets/"

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

            Interactions = {}

            for sharing in instance["ChatgptSharing"]:
                if sharing["Status"] == 404:
                    break
                
                if "NumberOfPrompts" not in sharing.keys():
                    continue
    
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

def calculate_cosine_similarity(Answers):

    conv_similarity = []
    for i in range(1, len(Answers)):    
        vectorizer = CountVectorizer().fit_transform([Answers[i-1],Answers[i]])
        vectors = vectorizer.toarray()
        similarity = cosine_similarity([vectors[0]], [vectors[1]])
        conv_similarity.append(similarity[0][0])
        
    return mean(conv_similarity)

def calculate_deviation(dataset,name,threshold):

    result = []
    Conversations = dataset["ChatgptConversations"]        
    avg_conversation_similarity = []
    for conversation in Conversations:
        conv_similarity = calculate_cosine_similarity(conversation["Answers"])
        avg_conversation_similarity.append(conv_similarity)

    for i in range(0,len(avg_conversation_similarity)):

        if avg_conversation_similarity[i] < threshold:
            result.append("Yes")
        else:
            result.append("No")
    
    return result      
    
def plot_pie_chart(data,datset_name):
    count = 0
    labels = ["Deviated","Not Deviated"]
    values = []
    for i in range(0,len(data)):
        if data[i] == "Yes":
            count = count + 1  
    dev_percentage = (count/len(data)) * 100 
    values.append(dev_percentage)
    values.append(100 - dev_percentage)
    plt.title('Pie Chart for Deviations in '+ datset_name)  
    plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=90, colors=['orange','blue'])

# Plotting bar graph with labels

def plot_bar_chart(data):

    x_labels = ['commit_sharings','pr_sharings','issues_sharings','discussion_sharings','hn_sharings']
    deviation_percentages = []
    for dataset in data.keys():
        res = data[dataset]
        count = 0
        for i in range(0,len(res)):
            if res[i] == "Yes":
                count = count + 1  
        dev_percentage = (count/len(res)) * 100
        deviation_percentages.append(dev_percentage)
    plt.bar(x_labels,deviation_percentages,color='blue')
    plt.xlabel('Datasets')
    plt.ylabel('Percentages')
    plt.title('Deviation Percentage by Dataset')
    plt.ylim(0, 100)
    for i, percentage in enumerate(deviation_percentages):
        plt.text(i, percentage + 2, f'{percentage:.2f}%', ha='center')

    plt.show()
    
def analyze_data():
    
    similarity_threshold = 0.5
    filepaths=[]
    values = {}
    for dataset in DATASET_CATEGORIES:
        file = glob(f"{CURRENT_DIRECTORY}{OUTPUT_FOLDER_PATH}{dataset.lower().replace(' ','_')}.json")
        dataset_name = dataset.lower().replace(' ','_')
        filepaths.append(file[0])

    data = [read_json_data(filepath) for filepath in filepaths]

    for i in range(0,len(data)):
        dataset_name = DATASET_CATEGORIES[i].lower().replace(' ','_')              
        res = calculate_deviation(data[i],dataset_name,similarity_threshold)        
        values[dataset_name] = res
        # plot_pie_chart(res,dataset_name)
    plot_bar_chart(values)
    plt.show()

def prepare_datasets():

    for file in DATASET_CATEGORIES:
        filepaths = glob(f"{CURRENT_DIRECTORY}{RAW_DATASETS_FILE_PATTERN}{file.lower().replace(' ','_')}.json")
        data = [read_json_data(filepath) for filepath in filepaths]
        processed_data = preprocess_data(data)
        write_data(processed_data,file)

def main():
    while(True):
        choice = input("\n1. Data Processing\n2. Data Analysis\n3. Exit\nEnter choice: ")

        if choice == "1":
            prepare_datasets()
        elif choice == "2":
            analyze_data()
        else:
            break

main()