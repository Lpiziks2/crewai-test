from typing import Dict, Any, Optional
from pydantic import BaseModel
from crewai.tools import BaseTool
import os
from datetime import datetime
import json

class ReportGenerationSchema(BaseModel):
    analysis_results: Optional[str] = None
    recommendations: Optional[str] = ""
    dataset_quality: Optional[str] = ""
    potential_uses: Optional[str] = ""
    output_dir: Optional[str] = "reports"

class ReportGenerationTool(BaseTool):
    name: str = "Report Generation Tool"
    description: str = "Generates a markdown EDA report."
    args_schema: type[ReportGenerationSchema] = ReportGenerationSchema

    def _run(self, analysis_results: str = None, recommendations: str = "", 
             dataset_quality: str = "", potential_uses: str = "",
             output_dir: str = "reports") -> str:
        try:
            # Create output directory with absolute path
            output_dir = os.path.abspath(output_dir)
            os.makedirs(output_dir, exist_ok=True)
            report_path = os.path.join(output_dir, f"eda_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")
            
            # Parse analysis results
            if isinstance(analysis_results, str):
                try:
                    analysis_data = json.loads(analysis_results)
                except json.JSONDecodeError:
                    analysis_data = {}
            else:
                analysis_data = {}
            
            # Extract report sections with safe fallbacks
            basic_info = analysis_data.get("basic_info", {})
            missing_values = analysis_data.get("missing_values", {})
            numeric_stats = analysis_data.get("numeric_stats", {})
            correlation = analysis_data.get("correlation", {})
            
            def format_number(value, decimals=2):
                """Helper function to safely format numbers"""
                try:
                    return f"{float(value):.{decimals}f}" if isinstance(value, (int, float)) else "N/A"
                except:
                    return "N/A"
            
            # Generate default dataset quality summary if none provided
            if not dataset_quality:
                missing_percent = missing_values.get("total_missing_percent", 0)
                if missing_percent < 5:
                    dataset_quality = "The dataset appears to be relatively clean with minimal missing values. Further analysis is recommended to identify potential outliers or inconsistencies."
                elif missing_percent < 15:
                    dataset_quality = "The dataset has a moderate amount of missing values that may require attention before modeling. Consider imputation strategies or feature removal."
                else:
                    dataset_quality = "The dataset contains a significant number of missing values which may impact analysis quality. Careful preprocessing is recommended."

            # Generate default potential uses if none provided
            if not potential_uses:
                potential_uses = "Based on the dataset structure, it could be suitable for descriptive analytics and exploratory visualizations. Further domain knowledge is required to determine specific use cases."
            
            # Build report content with enhanced formatting
            report_content = [
                "# 📊 Exploratory Data Analysis Report",
                f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
                "",
                "## 📋 Executive Summary",
                "This report provides a comprehensive analysis of the dataset, including basic statistics, missing value analysis, and correlation patterns.",
                "",
                "## 1️⃣ Dataset Overview",
                "### 📊 Basic Information",
                f"- **Total Records**: {basic_info.get('num_rows', 'N/A')}",
                f"- **Total Features**: {basic_info.get('num_columns', 'N/A')}",
                f"- **Memory Usage**: {format_number(basic_info.get('memory_usage', 0))} MB",
                "",
                "### 🏷 Column Information",
                "The following table shows the data types of each column in the dataset:",
                "",
                "| Column | Data Type | Description |",
                "|--------|-----------|-------------|"]
            
            # Add column information
            for col, dtype in basic_info.get("column_dtypes", {}).items():
                report_content.append(f"| {col} | {dtype} |")
            
            # Add dataset quality summary section
            report_content.extend([
                "",
                "### 🔍 Dataset Quality Summary",
                dataset_quality,
                ""
            ])
            
            # Add missing values section
            report_content.extend([
                "## 2️⃣ Missing Values Analysis",
                f"- **Total Missing**: {missing_values.get('total_missing', 'N/A')}",
                "",
                "| Column | Missing Count | Missing % |",
                "|--------|---------------|------------|"]
            )
            
            for col in missing_values.get("missing_by_column", {}):
                count = missing_values["missing_by_column"][col]
                percentage = missing_values.get("missing_percentage", {}).get(col, 0)
                report_content.append(
                    f"| {col} | {count} | {format_number(percentage)}% |")
            
            # Add numeric statistics section
            report_content.extend([
                "",
                "## 3️⃣ Numeric Column Analysis"])
            
            for col, stats in numeric_stats.get("statistics", {}).items():
                report_content.extend([
                    f"### {col}",
                    f"- **Mean**: {format_number(stats.get('mean'))}",
                    f"- **Median**: {format_number(stats.get('median'))}",
                    f"- **Std Dev**: {format_number(stats.get('std'))}",
                    f"- **Min**: {format_number(stats.get('min'))}",
                    f"- **Max**: {format_number(stats.get('max'))}",
                    f"- **Q1**: {format_number(stats.get('q1'))}",
                    f"- **Q3**: {format_number(stats.get('q3'))}",
                    ""])
            
            # Add correlation matrix section
            if correlation and "matrix" in correlation:
                report_content.extend([
                    "## 4️⃣ Correlation Analysis",
                    "| Variable 1 | Variable 2 | Correlation |",
                    "|------------|------------|-------------|"]
                )
                
                matrix = correlation["matrix"]
                for var1 in matrix:
                    for var2 in matrix[var1]:
                        if var1 != var2:  # Skip self-correlations
                            corr_value = matrix[var1][var2]
                            report_content.append(
                                f"| {var1} | {var2} | {format_number(corr_value)} |")
            
            # Add potential use cases section
            report_content.extend([
                "",
                "## 5️⃣ Potential Use Cases",
                potential_uses,
                ""
            ])
            
            # Add recommendations section
            report_content.extend([
                "## 6️⃣ Recommendations",
                recommendations or "No specific recommendations provided."])
            
            # Save report
            with open(report_path, 'w') as f:
                f.write("\n".join(report_content))
            
            return report_path
        
        except Exception as e:
            error_report_path = os.path.join(output_dir, "error_report.md")
            with open(error_report_path, 'w') as f:
                f.write(f"# ❌ Error in Report Generation\n\n{str(e)}")
            return error_report_path