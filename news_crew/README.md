# News Research Assistant 📰🔍

A powerful AI-driven news research tool that helps you gather, analyze, and generate comprehensive reports on any topic from recent news sources.

## Features

- **Automated Research**: Searches and analyzes news from the past 30 days
- **Comprehensive Reports**: Generates well-structured reports with key highlights and detailed analysis
- **Multiple Formats**: Supports both Markdown and plain text report formats
- **Web Interface**: User-friendly Streamlit-based web interface
- **Source Attribution**: Includes references and citations for all information

## Prerequisites

- Python 3.12 or higher
- EXA API key for news search functionality

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd news_crew
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and add your EXA API key:
   ```
   EXA_API_KEY=your_api_key_here
   ```

## Usage

### Web Interface

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Open your browser and navigate to the displayed URL (typically http://localhost:8501)

3. Enter your research topic and select your preferred report format

4. Click "Start Research" to generate your report

### Command Line Interface

Alternatively, you can use the command-line interface:

```bash
python main.py
```

## Configuration

The application uses several YAML configuration files:

- `config.yaml`: General application settings and API configurations
- `agents.yaml`: AI agent roles and capabilities
- `tasks.yaml`: Task definitions and output specifications

## Project Structure

```
├── app.py              # Streamlit web application
├── main.py             # Command-line interface
├── config.yaml         # Configuration settings
├── agents.yaml         # Agent definitions
├── tasks.yaml          # Task specifications
├── tools/
│   ├── report_generator.py  # Report generation tool
│   └── search_tools.py      # Search functionality
```

## Features in Detail

### Search Capabilities
- Searches news from the last 30 days
- Utilizes EXA search API for comprehensive coverage
- Includes content scraping for detailed analysis

### Report Generation
- Structured format with key highlights
- Full detailed analysis
- Source attribution and citations
- Related topics and implications
- Available in both Markdown and plain text formats

### AI Agents
- Search Agent: Specializes in finding and analyzing recent information
- Report Agent: Focuses on organizing and presenting information clearly

