#This code is used to plot graphs.

import json
import matplotlib.pyplot as plt
import os
import numpy as np

CURRENT_DIRECTORY = os.getcwd()
DATASET_CATEGORIES = [
    "Commit Sharings",
    "PR Sharings",
    "Issue Sharings",
    "Discussion Sharings",
    "HN Sharings"
]

output_folder_path = f'{CURRENT_DIRECTORY}/src/sentiment_analysis_results/'

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Using Pie chart to visualize the results
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
    plt.pie(sizes, pctdistance=1.1, labels=None, autopct=lambda p: '{:.0f}'.format(p * sum(sizes) / 100), startangle=90)

    # Add legend outside the pie chart
    plt.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5))
    plt.title("Distribution of Emotion Labels for " + file)



#Bar chart with max label for all data set
def count_max_label_2(data):
    # Create a dictionary to store the count of each emotion label
    emotion_counts = {item["label"]: 0 for dataset in data for item in dataset}

    # Iterate through the data to count the occurrences of each emotion label
    for dataset in data:
        max_item = max(dataset, key=lambda x: x["score"])
        emotion_counts[max_item["label"]] += 1

    # Find the label with the maximum count
    max_label = max(emotion_counts, key=emotion_counts.get)
    max_count = emotion_counts[max_label]

    return max_label, max_count

def plot_dataset_bargraph(categories, max_labels, max_counts):
    plt.figure(figsize=(10, 6))
    bars = plt.bar(categories, max_counts, color='skyblue')

    # Add labels for each bar
    for bar, label in zip(bars, max_labels):
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.1, label, ha='center', va='bottom')

    plt.xlabel('Dataset Categories')
    plt.ylabel('Count of Maximum Label')
    plt.title('Maximum Label Count for Each Dataset Category')
    plt.show()


def count_max_label_3(data):
    # Create a dictionary to store the count of each emotion label
    emotion_counts = {item["label"]: 0 for dataset in data for item in dataset}

    # Iterate through the data to count the occurrences of each emotion label
    for dataset in data:
        max_item = max(dataset, key=lambda x: x["score"])
        emotion_counts[max_item["label"]] += 1

    return emotion_counts

def main():
    while True:
        print("\nMenu:")
        print("1. Pie chart for Emotion Labels Distribution")
        print("2. Bar chart for Emotion Labels Distribution per Category")
        print("3. Bar chart for Maximum Label Count")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == "1":
            # Pie chart for Emotion Labels Distribution
            for file in DATASET_CATEGORIES:
                file_location = output_folder_path + file.lower().replace(' ', '_') + ".json"
                data = load_json(file_location)
                count_and_plot_emotion_labels(data, file)
            plt.show()

        elif choice == "2":
            # Bar chart for Emotion Labels Distribution per Category
            emotion_counts_per_category = {category: {} for category in DATASET_CATEGORIES}

            for file in DATASET_CATEGORIES:
                file_location = output_folder_path + file.lower().replace(' ', '_') + ".json"
                data = load_json(file_location)
                emotion_counts = count_max_label_3(data)
                emotion_counts_per_category[file] = emotion_counts

            categories = list(emotion_counts_per_category.keys())
            emotions = set(emotion for counts in emotion_counts_per_category.values() for emotion in counts.keys())

            bar_width = 0.2
            num_categories = len(categories)
            num_emotions = len(emotions)
            total_bar_width = bar_width * num_categories
            bar_positions = np.arange(num_emotions) * (total_bar_width + 0.2)

            for i, (category, counts) in enumerate(emotion_counts_per_category.items()):
                counts_list = [counts[emotion] for emotion in emotions]
                plt.bar(
                    bar_positions + i * bar_width,
                    counts_list,
                    bar_width,
                    label=category
                )

            plt.xlabel('Emotion Labels')
            plt.ylabel('Count')
            plt.title('Count of Emotion Labels for Each Dataset Category')
            plt.legend()
            plt.xticks(bar_positions + total_bar_width / 2, emotions)
            plt.tight_layout()
            plt.show()


        elif choice == "3":
            # Bar chart for Maximum Label Count
            category_labels = []
            max_labels = []
            max_label_counts = []

            for file in DATASET_CATEGORIES:
                file_location = output_folder_path + file.lower().replace(' ', '_') + ".json"
                data = load_json(file_location)
                max_label, max_count = count_max_label_2(data)
                category_labels.append(file)
                max_labels.append(max_label)
                max_label_counts.append(max_count)

            plot_dataset_bargraph(category_labels, max_labels, max_label_counts)

        elif choice == "4":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
