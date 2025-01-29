import os
import sys
from pathlib import Path

# Set the package root path to the desired directory
PACKAGE_ROOT = Path(__file__).resolve().parent.parent  # Moves up 1 level from 'config'
# print("Package Root:", PACKAGE_ROOT)

# Add the project root directory (the parent of 'src') to sys.path with priority
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))  # Insert at the beginning for priority

# Define folder paths
DATA_PATH = PACKAGE_ROOT / 'data'         # Path to the data folder
METADATA_PATH = PACKAGE_ROOT / 'metadata' # Path to the metadata folder

# Ensure the folders exist (optional, to prevent runtime issues)
DATA_PATH.mkdir(exist_ok=True)
METADATA_PATH.mkdir(exist_ok=True)

# print("Data Path:", DATA_PATH)
# print("Metadata Path:", METADATA_PATH)
# print("Sys Path:", sys.path)
