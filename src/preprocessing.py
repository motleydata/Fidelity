# generate function for preprocessing the data
import sys
from pathlib import Path
# Set the package root path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
    
from src.save_metadata import load_metadata
import pandas as pd
import datetime
import numpy as np

def create_dataframe(metadata):
    # Extract the files_metadata list
    files_metadata = metadata['files_metadata']

    # Create a DataFrame from the list
    df = pd.DataFrame(files_metadata)

    return df


def calculate_metrics(df):
    # Calculate the number of data sources
    number_of_datasources = len(df)
    
    # Calculate the average data age in months
    try:
        df['data_age'] = pd.to_timedelta(df['data_age'], errors='coerce')
        df['data_age_months'] = df['data_age'].apply(lambda x: x / pd.Timedelta(days=30))
        avg_data_age = df['data_age_months'].mean()
    except Exception as e:
        print(f"Error converting data_age to months: {e}")
        avg_data_age = None
    
    # Calculate the number of years of data used
    number_of_years_data = df['num_years_data'].mean()
    
    # Calculate the start and end year
    start_year = df['first_year'].min()
    end_year = df['last_year'].max()
    
    # Convert credibility_score to numeric, coercing errors
    df['credibility_score'] = pd.to_numeric(df['credibility_score'], errors='coerce')
    
    # Calculate the credibility scores
    max_credibility_score = df['credibility_score'].max()
    min_credibility_score = df['credibility_score'].min()
    avg_credibility_score = df['credibility_score'].mean()
    
    # Get the columns that are the same across all data sources
    common_columns = set.intersection(*df['columns'].apply(set))
    # Get all columns
    all_columns = set.union(*df['columns'].apply(set))
    
    # Get the uncommon columns
    uncommon_columns = all_columns - common_columns
    
    # Count the number of data sources with columns containing 'market_share'
    market_share_count = df['columns'].apply(lambda cols: any('market_share' in col for col in cols)).sum()
    
    # Prepare the metrics dictionary
    metrics = {
        'data_source_names': df['file_name'].tolist(),
        #get the same columns name from the metadata
        'common_columns': list(common_columns),
        'uncommon_columns': list(uncommon_columns),
        'number_of_sources': number_of_datasources,
        'avg_data_age_months': avg_data_age,
        'number_of_years': number_of_years_data,
        'start_year': start_year,
        'end_year': end_year,
        'max_credibility_score': max_credibility_score,
        'min_credibility_score': min_credibility_score,
        'avg_credibility_score': avg_credibility_score,
        'market_share_count': market_share_count
    }
    
    return metrics

