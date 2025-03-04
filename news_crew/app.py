import streamlit as st
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import yaml
from datetime import datetime, timedelta
import string
import time



# Import custom tools
from tools.report_generator import ReportGeneratorTool
from tools.search_tools import create_exa_tool, create_scrape_tool

# Set page configuration
st.set_page_config(
    page_title="News Research Assistant",
    page_icon="📰",
    layout="wide"
)

# Load environment variables
load_dotenv()

def load_yaml_with_env(file_path):
    """Load YAML file and replace environment variables"""
    with open(file_path, 'r') as file:
        content = file.read()
    
    # Create template with replacements
    template = string.Template(content)
    
    # Calculate date 30 days ago
    thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Create replacements dictionary
    replacements = {
        'EXA_API_KEY': os.getenv('EXA_API_KEY'),
        'THIRTY_DAYS_AGO': thirty_days_ago
    }
    
    # Apply replacements and load as YAML
    processed_content = template.substitute(replacements)
    return yaml.safe_load(processed_content)

def initialize_crew():
    """Initialize the crew with agents and tools"""
    # Load configurations
    config = load_yaml_with_env('config.yaml')
    agents_config = load_yaml_with_env('agents.yaml')
    tasks_config = load_yaml_with_env('tasks.yaml')
    
    # Create tools
    tools = {
        'exa_search_tool': create_exa_tool(
            api_key=config['exa']['api_key'],
            content=config['exa']['content'],
            summary=config['exa']['summary'],
            type=config['exa']['type']
        ),
        'scrape_website_tool': create_scrape_tool(),
        'report_generator_tool': ReportGeneratorTool()
    }
    
    # Create agents
    agents = {}
    for agent_id, agent_config in agents_config.items():
        # Get agent's tools
        agent_tools = [tools[tool_id] for tool_id in agent_config.get('tools', [])]
        
        # Create agent
        agents[agent_id] = Agent(
            role=agent_config['role'],
            goal=agent_config['goal'],
            backstory=agent_config['backstory'],
            tools=agent_tools,
            verbose=agent_config.get('verbose', True),
            allow_delegation=agent_config.get('allow_delegation', False)
        )
    
    # Create tasks
    tasks = []
    for task_id, task_config in tasks_config.items():
        # Get agent for this task
        agent = agents[task_config['agent']]
        
        # Create task
        task = Task(
            description=task_config['description'],
            expected_output=task_config['expected_output'],
            agent=agent
        )
        tasks.append(task)
    
    # Create crew
    crew = Crew(
        agents=list(agents.values()),
        tasks=tasks,
        verbose=config['crew']['verbose'],
        process=getattr(Process, config['crew']['process'])
    )
    
    return crew

# Title and description
st.title("📰🔍 News Research Helper")

st.write("""
👋 Welcome to your personal **News Research Helper**! 🌍  
This tool **searches the web** for the latest new on any topic you're interested in.  

It gathers information from the **past 30 days**,  analyzes it, and  creates an **easy-to-read report** for you.  

Perfect for:  
-  **Staying informed** about current events  
-  **Researching topics** with reliable sources  
-  **Satisfying your curiosity** with in-depth insights  

Just enter your topic and let the research begin! 🚀 
""")



# Sidebar for options
st.sidebar.title("Search Options")

# Sidebar for user inputs
search_topic = st.sidebar.text_input(
    "What would you like to research?",
    placeholder="Type a topic (e.g., climate change, space exploration)"
)

# Format selection - fixed option name
report_format = st.sidebar.selectbox(
    "How would you like your report?",
    options=["Markdown (formatted)", "Plain Text"],
    index=0
)

# Search button
search_button = st.sidebar.button("Start Research", type="primary")



# Display credits
st.sidebar.markdown("---")
st.sidebar.markdown("Your report will include news from the last 30 days")

# Initialize session state to store results
if 'report' not in st.session_state:
    st.session_state.report = None
if 'search_in_progress' not in st.session_state:
    st.session_state.search_in_progress = False

# Handle search action
if search_button and search_topic and not st.session_state.search_in_progress:
    st.session_state.search_in_progress = True
    
    # Initialize progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Update status
        status_text.text("Initializing research crew...")
        progress_bar.progress(10)
        time.sleep(0.5)
        
        # Initialize the crew
        crew = initialize_crew()
        
        # Update status
        status_text.text("Searching for latest information...")
        progress_bar.progress(30)
        time.sleep(0.5)
        
        # Use fixed 30-day date range (removed user selection)
        custom_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        question = f"{search_topic} (since {custom_date})"
            
        # Update status
        status_text.text("Analyzing information and generating report...")
        progress_bar.progress(60)
        
        # Run the crew to get results
        result = crew.kickoff(inputs={"question": question})
        
        # Update progress
        progress_bar.progress(100)
        status_text.text("Report ready!")
        time.sleep(0.5)
        
        # Store the result in session state - convert CrewOutput to string
        if hasattr(result, 'raw_output'):
            st.session_state.report = str(result.raw_output)
        else:
            st.session_state.report = str(result)
        
        # Clear progress indicators
        status_text.empty()
        progress_bar.empty()
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
    finally:
        st.session_state.search_in_progress = False

# Display results if available
# Display results if available
if st.session_state.report:
    st.header(f"Report on: {search_topic}")
    
    # Remove any download button HTML if present in the report
    report_content = st.session_state.report
    if "Download Report" in report_content:
        # Simple approach to remove the button HTML (might need refinement)
        report_content = report_content.split("<button")[0]
    
    # Display in appropriate format based on selection
    if report_format == "Markdown (formatted)":
        st.markdown(report_content)
    else:  # Plain Text
        st.code(report_content, language=None)
    
    # Add download button
    st.download_button(
        label="Download Report",
        data=st.session_state.report,
        file_name=f"news_report_{search_topic.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.{'md' if report_format == 'Markdown (formatted)' else 'txt'}",
        mime="text/markdown" if report_format == "Markdown (formatted)" else "text/plain"
    )
else:
    # Show instructions if no search has been performed
    if not search_button:
        st.info("👈 Enter a news topic and click 'Start Research' to get started")  # Fixed button name