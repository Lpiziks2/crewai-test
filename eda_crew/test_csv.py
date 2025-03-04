import os
import pandas as pd

def validate_csv_path(file_path: str) -> tuple[bool, str]:
    """
    Validates if the given file path exists and is a valid CSV file.
    
    Args:
        file_path (str): Path to the CSV file to validate
        
    Returns:
        tuple[bool, str]: A tuple containing:
            - bool: True if the file exists and is a valid CSV, False otherwise
            - str: Error message if validation fails, empty string if successful
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"
        
    # Check if it's a file (not a directory)
    if not os.path.isfile(file_path):
        return False, f"Path is not a file: {file_path}"
        
    # Check if file has .csv extension
    if not file_path.lower().endswith('.csv'):
        return False, f"File is not a CSV file: {file_path}"
        
    try:
        # Try to read the CSV file
        pd.read_csv(file_path)
        return True, ""
    except Exception as e:
        # If there's any error reading the CSV file
        return False, f"Error reading CSV file: {str(e)}"