# CEN5035 – Software Engineering – Fall 2023

Project by,
1. Rohit Natesh
2. Akhil Gorthi Bala Sai
3. Avaneeshakrishna Shastry Chakracodi

## Research Questions
The three research questions being explored in this project are,
1. Do ChatGPT conversations tend to deviate?
2. Which programming languages do developers ask ChatGPT for help with, and how does this pattern change over time?
3. While interacting with ChatGPT, what emotions do developers generally display?

## Project Structure
- `requirements.txt` has all the dependencies required to run the Python code.
- The `src` folder has all the code, data and the results.
- Under `src`, `raw_datasets` has all the DevGPT snapshots and files.
- Under `src`, each of the research questions are grouped under the folders `rq1`, `rq2` and `rq3` respectively.

### Files in `src/rq1`
- `src/rq1/main.py` is the main Python file having all the data processing and analysis code.
- Running the main file, it provides the user with options of data processing and data analysis.
    1. **Data processing** - Reads all the given datasets present in the `src/raw_datasets` and retrieves the relevant information for answering rq1. It cleans the data and prepares the data for further analysis. The resultant data is being merged from all the snapshots and placed under the folder `src/rq1/processed_datasets`.
    2. **Data analysis** - The data is read from the processed datasets, cosine similarity is used for determining the similarity and average metric is used for similarity metric for a conversation. Based on the threshold, bar graph and pie chart are plotted for each of the datasets to determine the deviation observed accordingly and the resulting graphs are stored under `src/rq1/results` 

### Files in `src/rq2`
- `src/rq2/main.py` is the main Python file having all the data processing and analysis code.
- Running the main file, gives the user menu driven options to run,
    1. **Data processing** - Reads all the raw datasets under `src/raw_datasets` and extracts all the required information, cleans the data, and prepares the data for further analysis. The processed data is grouped by category (eg- PR Sharings) from all the snapshots are stored as CSV files under `src/rq2/processed_datasets` path. 
    2. **Data analysis** - Reads the processed datasets from `src/rq2/processed_datasets` and analyzes it to identify the top 5 programming languages in every category. With the analyzed data it plots a scatter plot and draws the best fit line. The graphs generated are saved under `src/rq2/results`.

### Files in `src/rq3`
- `src/rq3/main.py` is the entry Python file exposing a menu which will do the following,
    1. **Data processing** - The data processing code is in `src/rq3/data_processing.py`, which reads the raw datasets from `src/raw_datasets`, extracts relevant information, cleans it, and stores the processed data under `src/rq3/processed_datasets`. The raw data from all the snapshots are grouped by category and stored.
    2. **Sentiment analysis** - The sentiment analysis code is under `src/rq3/sentiment_analysis.py`, which reads the processed data from `src/rq3/processed_datasets` and passes it to a BERT based sentiment analysis model. The results of the model is stored under `src/rq3/sentiment_analysis_results`.
    3. **Plot results** - The code for plotting the results are stored under `src/rq3/result_plotting.py`, which reads the sentiment analysis results from `src/rq3/sentiment_analysis_results` and plots pie charts and bar graphs to visualize the results. The graphs generated are saved under `src/rq3/results`.


## Steps to run
1. Install the dependencies from the requirements file.
   ```bash
   pip install -r ./requirements.txt
   ```
2. To run the research questions,
    - Research question 1
        ```bash
        python ./src/rq1/main.py
        ```
    - Research question 2
        ```bash
        python ./src/rq2/main.py
        ```
    - Research question 3
        ```bash
        python ./src/rq3/main.py
        ```
3. Follow the menu options provided by each of the research questions to perform pre-processing, data analysis or graph plotting.
