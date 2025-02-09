

# Fidelity Score Project\

This project is designed to manage and process metadata related to specific datasets. This repository organizes the workflow into distinct components for configuration, data management, metadata handling, and classification tasks.

## Project Structure\

/Fidelity
├── config/
│   ├── config.py    
├── data/                   
├── metadata/
├── src/
|   ├── fidelity.py
│   ├── get_metadata.py
│   ├── save_metadata.py
│   ├── llm_functions.py
│   ├── preprocessing.py
├── main.py
├── README.md
└── requirements.txt


## Definition of each folder and python file\

### config/
**config.py**: This python file contains a configurational setting that is used across the project directory. It currently contain the path to each folder


### data/
The data folder is to store data from different data sources


### metadata/
This folder will store metadata from the data sources in data folder


### src/
This folder contains source codes   
**fidelity.py**: This python code store the functions to calculate and print fidelity scores  
**get_metdata.py**: This file store functions to extract metadata from different file extension
**save_metadata.py**: This code is how we save metadata.json file to metadata folder
**llm_functions.py**: This file contains two main functions to classify the query and to look up for data sources that match the query (specifically for product type)  
**preprocessing.py**: This file contains function to generate dataframe and to calculate the metrics of combining different data source  
                **Example** 
                Metrics: {'data_source_names': ['agg_table_allyears_20241122_survey_mascara.xlsx', 'agg_table_allyears_20241118_Nielsen_mascara.xlsx', 'avg_unit_price_mascara.csv', 'agg_table_allyears_20241119_Circana_mascara.xlsx'], 'common_columns': ['brand', 'year'], 'uncommon_columns': ['recorded_time', 'market_share_rev_pct', 'total_market_size_count', 'product_type', 'aur_yearly', 'aur_circana', 'parent_company', 'brand_tier', 'country', 'quarter', 'aur_nielsen', 'agg_level', 'source_file', 'market_share_pct', 'weighted_aur', 'market_share_unit_sold', 'market_share_unit_pct', 'product_category', 'total_market_size_rev'], 'number_of_sources': 4, 'avg_data_age_months': 2.656665703735854, 'number_of_years': 3.0, 'start_year': 2022, 'end_year': 2024, 'max_credibility_score': 90, 'min_credibility_score': 60, 'avg_credibility_score': 75.0, 'market_share_count': 3}  *


### main.py

This main.py serves as an entry points for python application. We can just run main.py input the query and get fidelity score calculation

    To run file type: python main.py 

#### Output after running main.py:  

**1 Example of when the query is specialized**
Metadata does not exist, generating metadata...
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_shoes_allyears_survey_20250116.csv
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_shoes_allyears_20250114_circana.csv
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241122_survey_mascara.xlsx
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241118_Nielsen_mascara.xlsx
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_shoes_allyears_20250114_nielsen.csv
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/avg_unit_price_shoes.csv
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/avg_unit_price_mascara.csv
Processing: /Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241119_Circana_mascara.xlsx
Metadata for all files has been saved to /Users/siriluk/Documents/Motley/Fidelity/metadata/metadata.json

Please enter your query: **What is the market share of mascara in the US?**\
specialized\
Fidelity Score = On\
File Path List: ['/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241122_survey_mascara.xlsx', '/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241118_Nielsen_mascara.xlsx', '/Users/siriluk/Documents/Motley/Fidelity/data/avg_unit_price_mascara.csv', '/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241119_Circana_mascara.xlsx']\
Include avg_unit_price.csv: False\
Files used: ['/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241122_survey_mascara.xlsx', '/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241118_Nielsen_mascara.xlsx', '/Users/siriluk/Documents/Motley/Fidelity/data/avg_unit_price_mascara.csv', '/Users/siriluk/Documents/Motley/Fidelity/data/agg_table_allyears_20241119_Circana_mascara.xlsx']\
Metrics: {'data_source_names': ['agg_table_allyears_20241122_survey_mascara.xlsx', 'agg_table_allyears_20241118_Nielsen_mascara.xlsx', 'avg_unit_price_mascara.csv', 'agg_table_allyears_20241119_Circana_mascara.xlsx'], 'common_columns': ['brand', 'year'], 'uncommon_columns': ['market_share_unit_sold', 'brand_tier', 'total_market_size_rev', 'market_share_pct', 'market_share_rev_pct', 'agg_level', 'product_type', 'aur_circana', 'parent_company', 'market_share_unit_pct', 'aur_yearly', 'quarter', 'aur_nielsen', 'recorded_time', 'country', 'source_file', 'weighted_aur', 'product_category', 'total_market_size_count'], 'number_of_sources': 4, 'avg_data_age_months': 2.656665703735854, 'number_of_years': 3.0, 'start_year': 2022, 'end_year': 2024, 'max_credibility_score': 90, 'min_credibility_score': 60, 'avg_credibility_score': 75.0, 'market_share_count': 3}\

Fidelity Score: 4.75 out of 5 High\

Audit Scores:
Completeness of Sources Score: 5 High\
Number of Sources Score: 5 High\
Average Sources Age Score: 5 High\
Credibility of Soures Score: 4 High


**2 Example of when the query is generic**
Metadata already exists in the folder\
Please enter your query: **Tell me about mascara**\
generic\
Fidelity Score = Off\