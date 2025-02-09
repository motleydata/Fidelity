import os
import pandas as pd
import pyarrow.parquet as pq
from pathlib import Path
import sys
import json

# Set the package root path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from config.config import DATA_PATH, METADATA_PATH
from get_metadata import get_file_metadata
from datetime import datetime


def serialize_metadata(obj):
    # Convert datetime and pandas Timestamp to string (ISO format)
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, pd.Timestamp):
        return obj.isoformat()
    elif isinstance(obj, pd.Timedelta):
        return str(obj)
    return obj  # Return other objects as they are


def save_metadata(metadata, file_name):
    # Serialize and save metadata
    with open(file_name, 'w') as json_file:
        json.dump(metadata, json_file, default=serialize_metadata, indent=4)


def load_metadata(file_name):
    with open(file_name, 'r') as json_file:
        return json.load(json_file)


# Function to save metadata for all files in the folder
def save_metadata_for_folder(data_folder_path, metadata_folder_path, credibility_scores, output_file='metadata.json'):
    metadata_list = []  # List to store metadata for all files

    # Loop through all files in the folder
    for file_name in os.listdir(data_folder_path):
        file_path = os.path.join(data_folder_path, file_name)

        # Check if it's a file (not a directory) and if it's of the correct type
        if os.path.isfile(file_path) and file_path.endswith(('.xlsx', '.csv', '.pdf')):
            print(f"Processing: {file_path}")
            # Get metadata for the file
            metadata = get_file_metadata(file_path)
            # Add credibility score to metadata
            credibility_score = credibility_scores.get(file_name, "unknown")  # Default to "unknown" if not found
            metadata['credibility_score'] = credibility_score
            metadata_list.append(metadata)

    # Construct the file path in the metadata folder
    output_path = os.path.join(metadata_folder_path, output_file)

    # Ensure the metadata directory exists
    os.makedirs(metadata_folder_path, exist_ok=True)

    # Save all collected metadata to a single JSON file in METADATA_PATH
    save_metadata({'files_metadata': metadata_list}, output_path)
    print(f"Metadata for all files has been saved to {output_path}")


# # Example usage
# if __name__ == "__main__":
#     # Define the folder path containing the files
#     data_folder_path = DATA_PATH  # Path to data files

#     # Define the folder path to save metadata
#     metadata_folder_path = METADATA_PATH  # Path to save metadata files

#     # Example credibility scores
#     credibility_scores = {
#         'agg_table_allyears_20241118_Nielsen.xlsx': 80,
#         'agg_table_allyears_20241119_Circana.xlsx': 90,
#         'agg_table_allyears_20241122_survey.xlsx': 60,
#         'avg_unit_price': 70,
#         # Add more files and their credibility scores as needed
#     }

#     # Save metadata for all files in the folder
#     save_metadata_for_folder(data_folder_path, metadata_folder_path, credibility_scores)