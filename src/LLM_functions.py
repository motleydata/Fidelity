# classificy query to generic and specialized using LLM
import pandas as pd
import openai
import os
from dotenv import load_dotenv
import json

import sys
from pathlib import Path
# Set the package root path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))

from config.config import METADATA_PATH
load_dotenv()
# get OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

def classify_query(query):
    prompt = f"""
    Classify the input query from user as "generic" or "specialized" based on these definitions:
    - generic: Questions that can be answered definitively, common knowledge or are widely available online without deep research.
    - specialized: Questions requiring specialized knowledge, subjective analysis, or specific research.

    Examples:
    What is the origin or brand/product? -> generic
    What is the parent company (owner) of (brand name)?  -> generic
    Are there any upcoming product launches, updates, or innovations planned for (brand name)? -> generic
    What is the year-over-year (YOY) market share? -> specialized
    Which products see the highest rate of repeat purchases? -> specialized
    What unmet needs or gaps exist in the market that could be exploited to increase our share? -> specialized
    What is market share of product in the US? -> specialized

    Now classify:
    Question: "{query}"

    Do not add description, just only provide if it is Generic & definitive response and Non-generic response
    """
    
    # Call OpenAI GPT-4 API
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages =[
            {"role": "system", "content": "You are an expert to identify the type of questions."},
            {
                "role": "user",
                "content": prompt
            }
            ],
            max_tokens=30,  # Limit the length of the response
            temperature=0,  # Set temperature to 0 for deterministic output
        )
    return response.choices[0].message.content


"""After we define the query, I want to also look up data in metadata.json file,
If any values have the word associate with query, we will only accumerate datasource with that word 
to be an answer for the query
"""
def LLM_lookup(query, metadata_file):
    metadata_path = os.path.join(METADATA_PATH, metadata_file)
    with open(metadata_path, 'r') as file:
        metadata = json.load(file)
    
    # print("Metadata:", metadata)
    
    #extract file names from metadata
    file_names = [file['file_name'] for file in metadata['files_metadata']]
    #print(file_names)

    prompt = f"""
    If the {query} is asking about (market share) of (product name) such as "mascara", "shoes", etc. 
    For example;
    - What is the market share of (product name) in the us?
    - What is the market share of (product name) by brands?
    
    please look at the {metadata} and find the data source that has the word (product name) in the {file_names} or in other.
    
    Return the data source file paths that have the word (product name) in the metadata as a json list.
    
    Do not add description, just only provide the list of file paths.
    """
    # Call OpenAI GPT-4 API
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages =[
            {"role": "system", "content": "You are an expert to identify the type of questions."},
            {
                "role": "user",
                "content": prompt
            }
            ],
            max_tokens=500,  # Increase the length of the response
            temperature=0,  # Set temperature to 0 for deterministic output
        )
    output = response.choices[0].message.content
    
    output_new = output.replace("```json", "").strip().replace("```", "").strip()
    parsed_list = json.loads(output_new) 
    # return file_list
    return parsed_list

#Enter query to classify
# if __name__ == "__main__":
#     query = input("Enter your query: ")
#     classification = classify_query(query)
#     print("Classification:", classification)
#     file_list = LLM_lookup(query, 'metadata.json')
#     print("File List:", file_list)
#     print("file_list_type",type(file_list))