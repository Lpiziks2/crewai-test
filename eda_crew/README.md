#  EDA Crew - Automated Exploratory Data Analysis Tool

EDA Crew is a powerful tool that automates exploratory data analysis using AI agents. It provides comprehensive analysis of CSV files, generating detailed reports with statistical insights and recommendations.

##  Features

- **Automated Data Analysis**: Performs comprehensive statistical analysis of CSV files
- **AI-Powered Insights**: Uses CrewAI agents to analyze data and provide recommendations
- **Detailed Reports**: Generates markdown reports with visualizations and insights
- **Multiple Interfaces**: Both CLI and web-based interfaces available
- **Smart Recommendations**: Provides data cleaning and feature engineering suggestions

##  Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd eda_crew
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

##  Usage

### Command Line Interface

Analyze a CSV file using the command line:

```bash
python main.py path/to/your/file.csv
```

### Web Interface

Start the web application:

```bash
streamlit run app.py
```

Then open your browser and navigate to the displayed URL (typically http://localhost:8501).

## 📋 Report Structure

The generated reports include:

1. **Dataset Overview**
   - Basic information (rows, columns, memory usage)
   - Column information and data types

2. **Missing Values Analysis**
   - Total missing values
   - Missing values by column

3. **Numeric Column Analysis**
   - Statistical measures (mean, median, std dev, etc.)
   - Distribution analysis

4. **Correlation Analysis**
   - Correlation matrix for numeric columns

5. **Potential Use Cases**
   - Suggested applications for the dataset

6. **Recommendations**
   - Data cleaning suggestions
   - Feature engineering opportunities

##  Project Structure

```
eda_crew/
├── app.py              # Streamlit web interface
├── main.py             # CLI entry point
├── crew.py             # CrewAI setup and configuration
├── tools/              # Analysis and reporting tools
│   ├── csv_tool.py     # CSV analysis functionality
│   └── report_tool.py  # Report generation
└── config/             # Configuration files
```

##  Technical Details

- Uses CrewAI for intelligent analysis
- Pandas for data manipulation
- Streamlit for web interface


##  Important Notes

- Ensure your CSV files are properly formatted
- Large files may take longer to process
- The web interface provides a more interactive experience
- Reports are saved in the 'reports' directory by default