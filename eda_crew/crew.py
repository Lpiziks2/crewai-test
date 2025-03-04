import os
from crewai import Crew, Agent, Task
from .tools.csv_tool import csv_analysis_tool
from .tools.report_tool import ReportGenerationTool

def create_eda_crew(csv_path):
    # Initialize tools
    csv_tool = csv_analysis_tool
    report_tool = ReportGenerationTool()
    
    # Create agents
    data_analyst = Agent(
        role="Data Analyst",
        goal="Analyze CSV files and provide detailed statistical insights",
        backstory="""You are an expert data analyst with years of experience in
        exploratory data analysis. You know how to extract meaningful insights
        from raw data and can identify patterns, outliers, and trends.""",
        verbose=True,
        allow_delegation=True,
        tools=[csv_tool]
    )
    
    data_consultant = Agent(
        role="Data Consultant",
        goal="Provide strategic recommendations based on data analysis",
        backstory="""You are a seasoned data consultant who specializes in
        providing actionable recommendations based on data analysis. You have
        helped many organizations improve their data quality and extract value
        from their datasets.""",
        verbose=True,
        allow_delegation=True,
        tools=[report_tool]
    )
    
    # Create tasks
    analyze_task = Task(
        description=f"""
        Analyze the CSV file located at {csv_path}.
        Perform comprehensive exploratory data analysis including:
        1. Basic statistics (mean, median, mode, std, etc.)
        2. Data distribution analysis
        3. Identify missing values and outliers
        4. Correlation analysis between features
        
        Return the analysis results as a properly formatted JSON string.
        """,
        agent=data_analyst,
        expected_output="A JSON string containing the complete analysis results"
    )
    
    recommend_task = Task(
        description="""
        Based on the analysis results (provided as a JSON string), generate comprehensive recommendations:
        1. Data cleaning steps (handling missing values, outliers, etc.)
        2. Feature engineering suggestions
        3. Potential analysis directions
        4. Data quality improvement recommendations
        
        Use the ReportGenerationTool to create a final markdown report incorporating both the analysis results 
        and your recommendations. The analysis_results parameter should be the JSON string from the previous task.
        
        Save this report to a file in the 'reports' directory and return the file path.
        """,
        agent=data_consultant,
        expected_output="Path to a comprehensive markdown report with all findings and recommendations",
        context=[analyze_task]
    )
    
    # Create and return the crew
    crew = Crew(
        agents=[data_analyst, data_consultant],
        tasks=[analyze_task, recommend_task],
        verbose=True
    )
    
    return crew