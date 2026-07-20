# Multi-Agent Research Assistant

An AI-powered research automation system built using a multi-agent architecture. The application uses specialized AI agents to search, analyze, write, and review research content, creating structured and high-quality research reports.

## Overview

The Multi-Agent Research Assistant simplifies the research process by dividing tasks between multiple AI agents. Each agent has a specific responsibility, allowing the system to perform research workflows more efficiently.

The system includes:

- Search Agent for gathering information
- Reader Agent for extracting and analyzing content
- Writer Agent for generating research reports
- Critic Agent for reviewing and improving results

## Features

- Multi-agent AI workflow
- Automated research generation
- Web information retrieval
- Content extraction and analysis
- AI-powered report writing
- Research quality evaluation
- Streamlit user interface
- Secure API key management using environment variables

## Architecture

The Multi-Agent Research Assistant follows a modular multi-agent architecture where each AI agent performs a specialized task in the research workflow.

```
                         User Query
                             |
                             v
                  +----------------------+
                  | Streamlit Interface  |
                  |       (app.py)       |
                  +----------------------+
                             |
                             v
                  +----------------------+
                  |  Research Pipeline   |
                  |    (pipeline.py)     |
                  +----------------------+
                             |
          -----------------------------------------
          |                  |                    |
          v                  v                    v

+----------------+  +----------------+  +----------------+
| Search Agent   |  | Reader Agent   |  | Writer Agent   |
|                |  |                |  |                |
| Web Research   |  | Data Analysis  |  | Report         |
| Information   |  | Content        |  | Generation     |
| Retrieval      |  | Extraction     |  |                |
+----------------+  +----------------+  +----------------+
          |                  |                    |
          -------------------+--------------------
                             |
                             v

                  +----------------------+
                  |    Critic Agent      |
                  |  Review & Improve    |
                  |  Generated Content  |
                  +----------------------+
                             |
                             v

                  +----------------------+
                  |  Final Research      |
                  |       Report         |
                  +----------------------+
```

### Agent Responsibilities

### Search Agent
- Searches the web for relevant information.
- Collects useful sources and research materials.
- Provides raw information for further processing.

### Reader Agent
- Processes collected information.
- Extracts important facts and insights.
- Converts raw data into structured knowledge.

### Writer Agent
- Generates a well-structured research report.
- Organizes information into meaningful sections.
- Produces the final draft.

### Critic Agent
- Reviews the generated report.
- Identifies missing information or improvements.
- Provides feedback to enhance output quality.

### Pipeline Flow

1. User submits a research topic through the Streamlit interface.
2. The pipeline manages communication between agents.
3. Search Agent gathers external information.
4. Reader Agent analyzes collected content.
5. Writer Agent creates the research document.
6. Critic Agent evaluates and improves the generated response.
7. The final research report is displayed to the user.

## Tech Stack

- Python
- LangChain
- LangChain Core
- OpenAI API
- Streamlit
- Python-dotenv
- Web Search Tools

## Project Structure

```
Multi-Agent-Research-Assistant/
│
├── app.py                  # Streamlit application interface
├── pipeline.py             # Main research workflow and agent pipeline
├── agents.py               # AI agent definitions and configurations
├── tools.py                # Web search and scraping utilities
│
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables and API keys
├── .gitignore              # Files excluded from Git tracking
├── README.md               # Project documentation
│
└── .venv/                  # Python virtual environment
```

## Installation

Follow these steps to set up the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/pritish73/Multi-Agent-Research-Assistant.git
```

Navigate to the project directory:

```bash
cd Multi-Agent-Research-Assistant
```

---

### 2. Create a Virtual Environment

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

#### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
.\.venv\Scripts\activate
```

#### Mac/Linux

```bash
source .venv/bin/activate
```

---

### 3. Install Dependencies

Install all required packages:

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Create a `.env` file in the project root directory:

```env
OPENAI_API_KEY=your_openai_api_key
SEARCH_API_KEY=your_search_api_key
```

Add your actual API keys to the `.env` file.

---

### 5. Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```
