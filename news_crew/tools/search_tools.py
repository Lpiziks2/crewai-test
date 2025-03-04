# This file imports and configures search tools
from crewai_tools import EXASearchTool, ScrapeWebsiteTool

def create_exa_tool(api_key, content=True, summary=True, type="keyword"):
    """Create and configure an EXA search tool"""
    return EXASearchTool(
        api_key=api_key,
        content=content,
        summary=summary,
        type=type
    )

def create_scrape_tool():
    """Create a website scraping tool"""
    return ScrapeWebsiteTool()