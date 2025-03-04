from crewai import Crew
from eda_crew.crew import create_eda_crew
import json

from eda_crew.test_csv import validate_csv_path

def run_eda_on_file(csv_path):
    """
    Run exploratory data analysis on the provided CSV file.
    
    Args:
        csv_path (str): Path to the CSV file
        
    Returns:
        str: The generated report content as a string
        
    Raises:
        ValueError: If the CSV file is invalid or not found
    """
    # Validate the CSV file
    is_valid, message = validate_csv_path(csv_path)
    if not is_valid:
        raise ValueError(message)
        
    # Create the EDA crew
    crew = create_eda_crew(csv_path=csv_path)
    
    # Run the crew with the CSV path as input
    result = crew.kickoff(inputs={"csv_path": csv_path})
    
    # Extract the report file path from the task output
    report_path = str(result.output if hasattr(result, 'output') else result.raw_output if hasattr(result, 'raw_output') else result).strip()
    
    # Read and return the report content
    try:
        with open(report_path, 'r') as f:
            return f.read()
    except Exception as e:
        raise ValueError(f"Failed to read report file: {str(e)}")


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_csv>")
        sys.exit(1)
        
    csv_path = sys.argv[1]
    try:
        report_content = run_eda_on_file(csv_path)
        print(report_content)
    except ValueError as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()