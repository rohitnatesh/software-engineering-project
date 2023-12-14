from transformers import pipeline
import json
import os 

sentiment_pipeline = pipeline("sentiment-analysis")


CURRENT_DIRECTORY = os.getcwd()
DATASET_CATEGORIES = [
   "Commit Sharings",
   "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
    "HN Sharings"
]

OUTPUT_FOLDER_PATH = "/src/rq3/sentiment_analysis_results/"

def write_to_file(data, output_file):
    file_location = CURRENT_DIRECTORY + OUTPUT_FOLDER_PATH  + output_file.lower().replace(' ','_') + ".json"
    with open(file_location, "w") as outfile:
        json.dump(data,outfile, indent=2)

folder_path = f'{CURRENT_DIRECTORY}/src/rq3/processed_datasets/'

def main(): 
    for file in DATASET_CATEGORIES:
        file_location = folder_path + file.lower().replace(' ','_') + ".json"
        #print(file_location)
        if os.path.exists(file_location):
            with open(file_location, "r") as json_file_hn:
                data = json.load(json_file_hn)
                final_data = []
                for arr in data:
                    trim_arr = arr[0:512]
                    final_data.append(trim_arr)

                #Hugging Face Pre-Trained Model

                classifier = pipeline("text-classification",model='bhadresh-savani/bert-base-uncased-emotion', return_all_scores=True)
                
                prediction = classifier(final_data)
                formatted_prediction = json.dumps(prediction, indent=2)
                #print(formatted_prediction)
                write_to_file(prediction, file)


