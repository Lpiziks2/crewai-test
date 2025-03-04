from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os
import yaml
from datetime import datetime, timedelta
import string

# Import custom tools
from tools.report_generator import ReportGeneratorTool
from tools.search_tools import create_exa_tool, create_scrape_tool

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

def main():
    # Load environment variables
    load_dotenv()
    
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
    
    # Run the crew
    while True:
        question = input("Input: ")
        if question.lower() in ['exit', 'quit', 'q']:
            break
        result = crew.kickoff(inputs={"question": question})
        print(result)

if __name__ == "__main__":
    main()