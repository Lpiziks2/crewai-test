from crewai.tools import BaseTool
from typing import Any, Dict, List, Union, Optional
import json
from datetime import datetime

class ReportGeneratorTool(BaseTool):
    name: str = "ReportGeneratorTool"
    description: str = "Provides structure for news-style reports from search results"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def _run(self, search_results: Union[str, Dict, List], report_format: str = "markdown", question: str = None) -> str:
        """
        Generate a structured template for a news report
        
        Args:
            search_results: The results from search or scraped content
            report_format: Format for the report (markdown, text)
            question: Original query or topic of the report
            
        Returns:
            A structured report template with placeholders
        """
        try:
            # Parse search results
            data = self._parse_input_data(search_results)
            
            # Add question to data if provided
            if question and isinstance(data, dict):
                data["question"] = question
                
            # Generate timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Generate the appropriate format
            if report_format.lower() == "markdown":
                return self._generate_markdown_template(data, timestamp)
            else:
                return self._generate_text_template(data, timestamp)
                
        except Exception as e:
            return f"Error generating report structure: {str(e)}"
    
    def _parse_input_data(self, search_results: Union[str, Dict, List]) -> Union[Dict, List]:
        """Simple parsing of input data"""
        if isinstance(search_results, str):
            try:
                return json.loads(search_results)
            except json.JSONDecodeError:
                return {"raw_content": search_results}
        return search_results
    
    def _extract_title(self, data: Union[Dict, List]) -> str:
        """Extract a basic title from data"""
        if isinstance(data, dict):
            for key in ['title', 'question', 'query']:
                if key in data and data[key]:
                    return data[key]
        
        if isinstance(data, list) and data:
            first_item = data[0]
            if isinstance(first_item, dict) and "title" in first_item:
                return first_item["title"]
        
        return "News Report"
    
    def _generate_markdown_template(self, data: Union[Dict, List], timestamp: str) -> str:
        """Generate a markdown report template with proper structure"""
        title = self._extract_title(data)
        
        template = f"# {title}\n\n"
        template += f"*Published: {timestamp}*\n\n"
        
        # Executive Summary
        template += "## Executive Summary\n\n"
        template += "Provide a comprehensive summary (200-300 words) of key developments here.\n\n"
        
        # Key Events and Analysis
        template += "## Key Events and Analysis\n\n"
        
        # Create event sections (5-7)
        for i in range(1, 6):
            template += f"### Event {i}: [Event Title]\n\n"
            template += "**Date**: [Event Date]\n\n"
            template += "[Detailed explanation of the event (200-300 words)]\n\n"
            template += "**Analysis**:\n\n"
            template += "- Event significance within broader context\n"
            template += "- Expert opinions and relevant data\n"
            template += "- Historical context where applicable\n\n"
            template += "**Source**: [Source Attribution]\n\n"
        
        # Implications and Outlook - seamless version without title
        template += "## Implications and Future Outlook\n\n"
        
        # Short-term implications - narrative style without bullet points
        template += "[Discuss immediate implications of current developments here, including relevant stakeholder impacts and anticipated responses in the coming weeks/months. Consider political, economic, social, and other relevant dimensions. Aim for a flowing narrative of 150-200 words.]\n\n"
        
        # Long-term outlook - narrative style
        template += "[Provide thoughtful analysis of potential longer-term trajectories based on current trends and historical patterns. Incorporate uncertainty where appropriate and consider multiple plausible futures. Discuss how key variables might influence outcomes over the next 1-5 years. Aim for a cohesive narrative of 200-250 words.]\n\n"
        
        # Expert predictions - integrated into narrative
        template += "[Weave relevant expert opinions and forecasts throughout this section, attributing insights to specific sources where possible. Include contrasting viewpoints if appropriate to provide a balanced perspective.]\n\n"
        
        # Sources
        template += "## Sources\n\n"
        
        # Add source placeholders
        source_count = min(5, len(data) if isinstance(data, list) else (len(data.get("results", [])) if isinstance(data, dict) and "results" in data else 3))
        for i in range(1, source_count + 1):
            template += f"- **[Publication {i}]** ([Date]): [Article Title](URL)\n"
        
        return template
    
    def _generate_text_template(self, data: Union[Dict, List], timestamp: str) -> str:
        """Generate a plain text report template with proper structure"""
        title = self._extract_title(data)
        
        template = f"{title.upper()}\n"
        template += f"{'=' * len(title)}\n\n"
        template += f"Published: {timestamp}\n\n"
        
        # Executive Summary
        template += "EXECUTIVE SUMMARY:\n"
        template += f"{'-' * 18}\n\n"
        template += "Provide a comprehensive summary (200-300 words) of key developments here.\n\n"
        
        # Key Events
        template += "KEY EVENTS AND ANALYSIS:\n"
        template += f"{'-' * 23}\n\n"
        
        # Create event sections (5-7)
        for i in range(1, 6):
            template += f"EVENT {i}: [EVENT TITLE]\n\n"
            template += "Date: [Event Date]\n\n"
            template += "[Detailed explanation of the event (200-300 words)]\n\n"
            template += "Analysis:\n"
            template += "- Event significance within broader context\n"
            template += "- Expert opinions and relevant data\n"
            template += "- Historical context where applicable\n\n"
            template += "Source: [Source Attribution]\n\n"
        
        # Implications - seamless version without subdivisions
        template += "IMPLICATIONS AND FUTURE OUTLOOK:\n"
        template += f"{'-' * 31}\n\n"
        
        # Integrated narrative style for implications and outlook
        template += "[Discuss immediate implications of current developments, including relevant stakeholder impacts and anticipated responses. Consider how these developments might unfold over time, from short-term consequences to longer-term trajectories. Include expert opinions and contrasting viewpoints where appropriate to provide a balanced perspective. Analyze potential futures based on current trends and historical patterns, incorporating uncertainty where appropriate. Aim for a cohesive narrative of 400-500 words that flows naturally between near-term implications and longer-term outlooks.]\n\n"
        
        # Sources
        template += "SOURCES:\n"
        template += f"{'-' * 8}\n\n"
        
        # Add source placeholders
        source_count = min(5, len(data) if isinstance(data, list) else (len(data.get("results", [])) if isinstance(data, dict) and "results" in data else 3))
        for i in range(1, source_count + 1):
            template += f"• [Publication {i}] ([Date]): [Article Title]. URL: [URL]\n"
        
        return template