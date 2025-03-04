import pandas as pd
import os
from typing import Dict, Any
from crewai.tools import tool

@tool
def csv_analysis_tool(csv_path: str) -> Dict[str, Any]:
    """
    Reads and analyzes a CSV file, performing basic Exploratory Data Analysis (EDA).
    
    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        Dict[str, Any]: A dictionary containing CSV insights, or an error message.
    """
    
    try:
        # Check if file exists
        if not os.path.exists(csv_path):
            return {"error": "File not found."}

        # Load CSV into DataFrame without any row limitations
        df = pd.read_csv(csv_path, low_memory=False)

        # Basic info
        basic_info = {
            "num_rows": int(df.shape[0]),
            "num_columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "column_dtypes": {col: str(df[col].dtype) for col in df.columns},
            "memory_usage": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        }

        # Numeric statistics
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        numeric_stats = {
            "statistics": {
                col: {
                    "mean": float(df[col].mean()),
                    "median": float(df[col].median()),
                    "std": float(df[col].std()),
                    "min": float(df[col].min()),
                    "max": float(df[col].max()),
                    "q1": float(df[col].quantile(0.25)),
                    "q3": float(df[col].quantile(0.75))
                } for col in numeric_cols
            }
        }

        # Correlation matrix for numeric columns
        correlation = {
            "matrix": df[numeric_cols].corr().to_dict()
        }

        # Missing values
        missing_values = {
            "total_missing": int(df.isnull().sum().sum()),
            "missing_by_column": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).round(2).to_dict()
        }

        return {
            "basic_info": basic_info,
            "numeric_stats": numeric_stats,
            "correlation": correlation,
            "missing_values": missing_values
        }

    except pd.errors.EmptyDataError:
        return {"error": "The file is empty."}
    except pd.errors.ParserError:
        return {"error": "Error parsing the CSV file. Check the format."}
    except Exception as e:
        return {"error": str(e)}