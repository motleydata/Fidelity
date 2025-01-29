import os
import pandas as pd
import openpyxl
import fitz  # PyMuPDF
import pyarrow.parquet as pq
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import sys

# Set the package root path
PACKAGE_ROOT = Path(__file__).resolve().parent.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
    
from config.config import DATA_PATH
# print("Metadata Path:", METADATA_PATH)
# print("Data Path:", DATA_PATH)
# print("Sys Path:", sys.path)

# Function to extract metadata from a file based on its type
def get_file_metadata(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension in ['.xlsx', '.xls']:
        return get_excel_metadata(file_path)
    elif file_extension == '.pdf':
        return get_pdf_metadata(file_path)
    elif file_extension == '.csv':
        return get_csv_metadata(file_path)
    elif file_extension == '.parquet':
        return get_parquet_metadata(file_path)
    elif file_extension == '.html' or file_extension.startswith('http'):
        return get_url_metadata(file_path)
    else:
        return {'file_name': os.path.basename(file_path), 'error': 'Unsupported file type'}

# Extract metadata from Excel files
def get_excel_metadata(file_path):
    file_name = os.path.basename(file_path)
    workbook = openpyxl.load_workbook(file_path)
    sheet_names = workbook.sheetnames

    sheet = workbook[sheet_names[0]]
    data = pd.DataFrame(sheet.values)
    data.columns = data.iloc[0]  # First row as header
    data = data.drop(0)  # Remove header row

    column_names = data.columns.tolist()

    # Initialize metadata variables
    last_recorded_time = None
    data_age = None
    first_year = None
    last_year = None
    num_years = None

    # Check if 'recorded_time' column exists and process
    if 'recorded_time' in column_names:
        data['recorded_time'] = pd.to_datetime(data['recorded_time'], errors='coerce')
        valid_times = data['recorded_time'].dropna()
        if not valid_times.empty:
            last_recorded_time = valid_times.max()
            data_age = pd.Timestamp.now() - last_recorded_time

    # Check if 'year' column exists and process
    if 'year' in column_names:
        data['year'] = pd.to_numeric(data['year'], errors='coerce')
        valid_years = data['year'].dropna()
        if not valid_years.empty:
            first_year = valid_years.min()
            last_year = valid_years.max()
            num_years = last_year - first_year + 1

    metadata = {
        'file_name': file_name,
        'file_path': file_path,
        'num_rows': len(data),
        'num_columns': len(data.columns),
        'columns': column_names,
        'last_recorded_time': last_recorded_time.isoformat() if last_recorded_time else None,
        'data_age': str(data_age) if data_age else None,
        'first_year': first_year,
        'last_year': last_year,
        'num_years_data': num_years
    }
    return metadata

# Extract metadata from PDF files
def get_pdf_metadata(file_path):
    file_name = os.path.basename(file_path)
    doc = fitz.open(file_path)
    metadata = doc.metadata
    metadata['file_name'] = file_name
    metadata['file_path'] = file_path
    return metadata

# Extract metadata from URLs
def get_url_metadata(url):
    file_name = os.path.basename(url) if url.startswith('http') else url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return {
        'file_name': file_name,
        'url': url,
        'title': soup.title.string if soup.title else 'No title',
    }

# Extract metadata from CSV files
def get_csv_metadata(file_path):
    file_name = os.path.basename(file_path)
    df = pd.read_csv(file_path)

    column_names = df.columns.tolist()

    # Initialize metadata variables
    last_recorded_time = None
    data_age = None
    first_year = None
    last_year = None
    num_years = None

    # Check if 'recorded_time' column exists and process
    if 'recorded_time' in column_names:
        df['recorded_time'] = pd.to_datetime(df['recorded_time'], errors='coerce')
        valid_times = df['recorded_time'].dropna()  # Exclude invalid/missing dates
        if not valid_times.empty:
            last_recorded_time = valid_times.max()
            data_age = pd.Timestamp.now() - last_recorded_time

    # Check if 'year' column exists and process
    if 'year' in column_names:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')  # Ensure numeric year values
        valid_years = df['year'].dropna()  # Exclude invalid/missing years
        if not valid_years.empty:
            first_year = int(valid_years.min())
            last_year = int(valid_years.max())
            num_years = last_year - first_year + 1

    # Create metadata dictionary
    metadata = {
        'file_name': file_name,
        'file_path': file_path,
        'num_rows': len(df),
        'num_columns': len(df.columns),
        'columns': column_names,
        'last_recorded_time': last_recorded_time.isoformat() if last_recorded_time else None,
        'data_age': str(data_age) if data_age else None,
        'first_year': first_year,
        'last_year': last_year,
        'num_years_data': num_years
    }
    return metadata

# Extract metadata from Parquet files
def get_parquet_metadata(file_path):
    file_name = os.path.basename(file_path)
    parquet_file = pq.ParquetFile(file_path)
    metadata = parquet_file.metadata
    return {
        'file_name': file_name,
        'file_path': file_path,
        'num_rows': metadata.num_rows,
        'num_columns': metadata.num_columns,
        'columns': [metadata.schema[i].name for i in range(metadata.num_columns)],
    }
    return metadata

# Main logic for testing (optional)
# if __name__ == "__main__":
#     test_file_path = str(DATA_PATH / "avg_unit_price.csv")  # Example file path
#     print(f"Metadata for {test_file_path}:")
#     print(get_file_metadata(test_file_path))
