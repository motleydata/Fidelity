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
from src.llm_functions import classify_query, LLM_lookup
from src.save_metadata import save_metadata_for_folder
from src.preprocessing import calculate_metrics
from src.fidelity import calculate_fidelity_score, fidelity_score_definition, print_fidelity_score


#1. Generate metadata from the file in DATA_PATH ('data')
#define the folder path containing the files
data_folder_path = DATA_PATH  # Path to data files

# Define the folder path to save metadata
metadata_folder_path = METADATA_PATH  # Path to save metadata files

# Example credibility scores for each file in DATA_PATH
credibility_scores = {
        'agg_table_allyears_20241118_Nielsen_mascara.xlsx': 80,
        'agg_table_allyears_20241119_Circana_mascara.xlsx': 90,
        'agg_table_allyears_20241122_survey_mascara.xlsx': 60,
        'avg_unit_price_mascara.csv': 70,
        'agg_table_shoes_allyears_20250114_circana.csv': 85,
        'agg_table_shoes_allyears_20250114_nielsen.csv': 75,
        'agg_table_shoes_allyears_survey_20250116.csv': 65,
        'avg_unit_price_shoes.csv': 95   
    }

#if metadata.json not exist in the folder or the metadata is different than the one we have, generate metadata for the folder using save
metadata_file_path = metadata_folder_path / 'metadata.json'

if not os.path.exists(metadata_file_path):
    print("Metadata does not exist, generating metadata...")
    new_metadata = save_metadata_for_folder(data_folder_path, metadata_folder_path, credibility_scores)
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

    # Select only metadata that have file_path presented in list generated from LLM to do dataframe
    file_path_list = LLM_lookup(query, str(file_path))
    print("File Path List:", file_path_list)
    
    # Only have metadata of the file_path_list
    with open(file_path, 'r') as file:
        metadata = json.load(file)
    filtered_metadata = [file for file in metadata['files_metadata'] if file['file_path'] in file_path_list]

    # Create a DataFrame from the filtered metadata
    df = pd.DataFrame(filtered_metadata)
    
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

    scores, fidelity_scores = calculate_fidelity_score(metrics)
    fidelity_score_def = fidelity_score_definition(fidelity_scores)
    print()
    print(f"Fidelity Score: {fidelity_scores} out of 5 {fidelity_score_def}")
    # Add new line
    print()
    # Print each score and definition of each criteria
    print("Audit Scores:")
    print_fidelity_score(scores)


