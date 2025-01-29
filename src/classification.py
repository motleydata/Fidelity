# classificy query to generic and specialized using LLM
import pandas as pd
import openai
import os
from dotenv import load_dotenv
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

#Enter query to classify
# if __name__ == "__main__":
#     query = input("Enter your query: ")
#     classification = classify_query(query)
#     print("Classification:", classification)
