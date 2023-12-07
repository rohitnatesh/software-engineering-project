# Using Pie chart to visualize the results

import json
import matplotlib.pyplot as plt

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def count_and_plot_emotion_labels(data, file):
    # Create a dictionary to store the count of each emotion label
    emotion_counts = {item["label"]: 0 for dataset in data for item in dataset}

    # Iterate through the data to count the occurrences of each emotion label
    for dataset in data:
        max_item = max(dataset, key=lambda x: x["score"])
        emotion_counts[max_item["label"]] += 1
    print("Emotion counts for "+file+"\n")
    print(emotion_counts)
    print("\n")
    # Plot the pie chart with count values on slices
    labels = list(emotion_counts.keys())
    sizes = list(emotion_counts.values())

    plt.figure(figsize=(8, 8))  # Adjust figure size as needed
    plt.pie(sizes, labels=None, autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100), startangle=90)

    # Add legend outside the pie chart
    plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("Distribution of Emotion Labels for " + file)


DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
    "HN Sharings"
]
output_folder_path = 'G:/FSU/Fall 2023/Software Engg/Project/Code/software-engineering-project/src/hugging_face_results/'

# Example usage
for file in DATASET_CATEGORIES:
    file_location = output_folder_path + file.lower().replace(' ', '_') + ".json"
    data = load_json(file_location)

    # Count and plot the occurrence of each emotion label using a pie chart with count values
    count_and_plot_emotion_labels(data, file)

# Show all pie charts at once
plt.show()
