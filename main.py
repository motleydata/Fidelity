#This is the main python file to run the project

import os
import sys
from pathlib import Path
import os
import pandas as pd
import json
from datetime import datetime

src_path = Path(__file__).resolve().parent / "src"
if str(src_path) not in sys.path:
    sys.path.append(str(src_path))

from config.config import DATA_PATH, METADATA_PATH
from src.classification import classify_query
from src.save_metadata import save_metadata_for_folder
from src.preprocessing import create_dataframe, calculate_metrics


#1. Generate metadata from the file in DATA_PATH ('data')
#define the folder path containing the files
data_folder_path = DATA_PATH  # Path to data files

# Define the folder path to save metadata
metadata_folder_path = METADATA_PATH  # Path to save metadata files

# Example credibility scores for each file in DATA_PATH
credibility_scores = {
        'agg_table_allyears_20241118_Nielsen.xlsx': 80,
        'agg_table_allyears_20241119_Circana.xlsx': 90,
        'agg_table_allyears_20241122_survey.xlsx': 60,
        'avg_unit_price.csv': 70,
    }

#if metadata.json not exist in the folder, generate metadata for the folder using save
if not os.path.exists(metadata_folder_path / 'metadata.json'):
    save_metadata_for_folder(data_folder_path, metadata_folder_path, credibility_scores)
else:
    print("Metadata already exists in the folder")


# 2. Get the query from the user
query = input("Please enter your query: ")

# Classify the query using the classify_query function
query_type = classify_query(query)
print(query_type)

# Check if the query type is 'specialized' to enable fidelity score
fidelity_score = False
if query_type == 'specialized':
    fidelity_score = True
    print("Fidelity Score = On")
else:
    print("Fidelity Score = Off")

# Only process metadata.json if fidelity_score is True
if fidelity_score:
    # Load the JSON data and create dataframe
    file_path = METADATA_PATH / 'metadata.json'
    df = create_dataframe(file_path)
    
    # Determine if avg_unit_price.csv should be included based on the query
    include_avg_unit_price = any(word in query.lower() for word in ['unit', 'units', 'unit sold'])

    # Debug print to check the query and inclusion condition
    print(f"Query: {query}")
    print(f"Include avg_unit_price.csv: {include_avg_unit_price}")  
    
    # Ensure the column contains only strings and strip any whitespace
    df['file_path'] = df['file_path'].astype(str).str.strip()

    # Apply the filtering to the DataFrame
    if not include_avg_unit_price:
        # Filter out 'avg_unit_price.csv' (case-insensitive)
        df = df[~df['file_path'].str.contains('avg_unit_price.csv', case=False)]

    # Print the filtered file names
    print("Files used:", df['file_path'].tolist())
    
    # Calculate and print metrics
    metrics = calculate_metrics(df)
    print("Metrics:", metrics)


#Formular to calculate fidelity score based on accumurate data source for the question
#3. Define a function to calculate fidelity score

def calculate_fidelity_score(metrics):
    scores = [] #list to store score for each criterias

    """1. data_source_names: Completeness of data sources
    If only data_source name has the word "survey"--> score = 1
    If Nielsen or Circana --> score = 3
    If both Nielsen and Circana --> score = 4
    if data_source name Nielsen,Circana and Survey --> 5"""

    data_source_names = set(name.lower() for name in metrics['data_source_names'])

    # Define presence flags
    has_nielsen = any("nielsen" in name for name in data_source_names)
    has_circana = any("circana" in name for name in data_source_names)
    has_survey = any("survey" in name for name in data_source_names)

    #print("Data Source Names:", data_source_names)

    # Determine score based on conditions
    if has_nielsen and has_circana and has_survey:
        scores.append(5)
    elif has_survey and not (has_nielsen or has_circana):
        scores.append(1)
    elif has_nielsen and not (has_circana or has_survey):
        scores.append(3)
    elif has_circana and not (has_nielsen or has_survey):
        scores.append(3)
    elif has_nielsen and has_circana and not has_survey:
        scores.append(4)

    print("Data Source Names Score:", scores)

    """2. number of sources: Quantity of data sources syndicated
    1 → score = 1
    2 → score = 3
    >3 → score = 5"""
    
   # 2. Quantity of data sources
    number_of_sources = metrics.get('number_of_sources', None)
    
    if number_of_sources is None:
        print("Warning: number_of_sources is missing or None")
    elif number_of_sources == 1:
        scores.append(1)
    elif number_of_sources == 2:
        scores.append(3)
    elif number_of_sources >= 3:
        scores.append(5)

    print("Number of Sources Score:", scores)


    """3. average data age(month): Recency/freshness of data source
    If a year or less → score = 5.
    If more than a year but less than 2 years → score = 4.
    More than 2 years less than 3 years → score = 3
    More than 3 years less than 5 years → score = 2
    More than 5 years → 1"""
    
    average_data_age = metrics['avg_data_age_months']
    #make sure average_data_age is not None and it is numerics
    if average_data_age is None:
        print("Error: Average Data Age (Months) is None")
        return None
    if average_data_age <= 12:
        scores.append(5)
    elif average_data_age <= 24:
        scores.append(4)
    elif average_data_age <= 36:
        scores.append(3)
    elif average_data_age <= 60:
        scores.append(2)
    else:    
        scores.append(1)
        
    print("Average Data Age Score:", scores)

    
    """4. credibility score: Credibility of data sources
        Min, Max, and Average credibility score use the same calculation
        >= 80 → score = 5,
        >= 70 and < 80 → score = 4,
        >=50 and <70 → score = 3,
        >= 30 < 50 → score = 2,
        < 30 → score = 1
    """
    
    def calculate_credibility_score(value):
        if value >= 80:
            return 5
        elif value >= 70:
            return 4
        elif value >= 50:
            return 3
        elif value >= 30:
            return 2
        else:
            return 1
    
    max_score = calculate_credibility_score(metrics['max_credibility_score'])
    min_score = calculate_credibility_score(metrics['min_credibility_score'])
    avg_score = calculate_credibility_score(metrics['avg_credibility_score'])
    
    #average credibility score from min, max and avg credibility score
    avg_credibility_score = (max_score + min_score + avg_score) / 3
    
    scores.append(avg_credibility_score)
    
    print("Credibility Score:", scores)
    
    print("list_score", scores)
    # calculate fidelity score by taking the average of all criterias
    fidelity_scores = sum(scores) / len(scores)
    
    #print("Number of Sources Score:", scores)
    return scores, fidelity_scores

#define function to give a name definition of fidelity score

def fidelity_score_definition(score):
    if score >= 4.0:
        return "High"
    elif score >= 3.0:
        return "Medium high"
    elif score >= 2.0:
        return "Medium"
    elif score >= 1.0:
        return "Medium low"
    else:
        return "Low"


#define function to print each score and definition in the list
criteria_name = ["Data Source Names", "Number of Sources", "Average Data Age", "Credibility Score"]

def print_fidelity_score(scores):
    #for each score, print criteria name, score and definition
    for i, score in enumerate(scores):
        print(f"{criteria_name[i]} Score:", score,fidelity_score_definition(score))
        # print(f"{criteria_name[i]} Score Definition:", fidelity_score_definition(score))
        print("\n")


if __name__ == "__main__":
    if fidelity_score:
        scores,fidelity_scores = calculate_fidelity_score(metrics)
        print("Fidelity Scores:", fidelity_scores)
        fidelity_score_def = fidelity_score_definition(fidelity_scores)
        print("Fidelity Score Definition:", fidelity_score_def)
        
        #print each score and definition of each criteria
        print_fidelity_score(scores)