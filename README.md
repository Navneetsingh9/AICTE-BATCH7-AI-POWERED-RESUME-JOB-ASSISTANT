# 📄 AI-POWERED RESUME & JOB ASSISTANT

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)](https://streamlit.io/)
[![OpenRouter](https://img.shields.io/badge/OpenRouter-Free%20API-green)](https://openrouter.ai/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

A powerful multi-agent AI system to help job seekers with resume optimization, cover letter generation, and interview preparation. Built with Python and Streamlit, powered by OpenRouter's free AI models.

<div align="center">
  <img src="https://img.icons8.com/color/96/000000/resume.png" alt="Resume Icon"/>
  <img src="https://img.icons8.com/color/96/000000/covering-letter.png" alt="Cover Letter Icon"/>
  <img src="https://img.icons8.com/color/96/000000/interview.png" alt="Interview Icon"/>
</div>

## 📋 Table of Contents
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

## ✨ Features

### 🤖 Agent 1: Resume Reviewer
| Feature | Description |
|---------|-------------|
| 📄 **PDF Upload** | Upload your resume in PDF format |
| ✏️ **Manual Entry** | Paste resume text directly |
| 📊 **ATS Analysis** | Get Applicant Tracking System feedback |
| 💪 **Strengths** | Identify what's working well |
| 🔧 **Improvements** | Actionable suggestions to enhance your resume |
| 🔑 **Keywords** | Get recommendations for ATS-friendly keywords |

### ✍️ Agent 2: Cover Letter Writer
| Feature | Description |
|---------|-------------|
| 🎯 **Job Targeting** | Customize for specific job titles |
| 🏢 **Company Specific** | Tailor to company culture |
| 🎭 **Tone Options** | Professional, Enthusiastic, or Creative |
| 📝 **Job Description** | Paste JD for better matching |
| 💾 **Download** | Save your cover letter as text file |

### 🎤 Agent 3: Interview Coach
| Feature | Description |
|---------|-------------|
| 📚 **40+ Questions** | Built-in interview question database |
| 🎯 **Role Specific** | Questions for Frontend, Backend, Python, etc. |
| 📊 **Difficulty Levels** | Easy, Medium, Hard questions |
| 💡 **STAR Method** | Behavioral question guidance |
| ✅ **Answer Feedback** | Get feedback on your practice answers |

## 🏗 Architecture
```mermaid
graph TB
    %% Frontend Layer
    subgraph Frontend [Streamlit Frontend]
        T1[Resume Reviewer Tab]
        T2[Cover Letter Writer Tab] 
        T3[Interview Coach Tab]
    end

    %% Agent Layer
    subgraph Agents [Multi-Agent System]
        BA[Base Agent]
        
        subgraph SpecificAgents [Specialized Agents]
            RA[Resume Reviewer Agent]
            CA[Cover Letter Writer Agent]
            IA[Interview Coach Agent]
        end
        
        BA --> RA
        BA --> CA
        BA --> IA
    end

    %% API Layer
    subgraph API [OpenRouter API]
        OR[openrouter/free Model]
        OR_Headers[HTTP Headers<br/>HTTP-Referer<br/>X-Title]
    end

    %% Data Sources
    subgraph Data [Data Sources]
        QC[Question Collector]
        FB[Fallback Questions<br/>40+ Built-in]
        PDF[PDF Resume Upload]
    end

    %% Connections
    T1 --> RA
    T2 --> CA
    T3 --> IA
    
    RA --> OR
    CA --> OR
    IA --> OR
    
    IA --> QC
    QC --> FB
    
    PDF --> T1
    PDF --> T2

    %% Styling
    classDef frontend fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef agent fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef api fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef data fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class T1,T2,T3 frontend
    class BA,RA,CA,IA agent
    class OR,OR_Headers api
    class QC,FB,PDF data
```

### Component Flow Diagram
```mermaid
flowchart LR
    User([User]) --> UI{Streamlit UI}
    
    UI --> Resume[Resume Reviewer]
    UI --> Cover[Cover Letter Writer]
    UI --> Interview[Interview Coach]
    
    Resume --> Agent1[Resume Agent]
    Cover --> Agent2[Cover Letter Agent]
    Interview --> Agent3[Interview Agent]
    
    Agent1 & Agent2 & Agent3 --> BaseAgent[Base Agent]
    
    BaseAgent --> OpenRouter[OpenRouter API]
    OpenRouter --> Models[openrouter/free]
    
    Agent3 --> QC[Question Collector]
    QC --> GitHub[GitHub Sources]
    QC --> Fallback[Fallback Questions<br/>40+ Built-in]
    
    Resume --> PDF[PDF Upload]
    
    style User fill:#f9f,stroke:#333,stroke-width:4px
    style OpenRouter fill:#9f9,stroke:#333,stroke-width:2px
    style Fallback fill:#ff9,stroke:#333,stroke-width:2px
```

### 🔄 Data Flow Diagram
```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Agent as Base Agent
    participant OpenRouter
    participant QC as Question Collector

    User->>UI: Upload Resume
    User->>UI: Select Action
    
    par Resume Review
        UI->>Agent: review_resume(text)
        Agent->>OpenRouter: API Call
        OpenRouter-->>Agent: AI Response
        Agent-->>UI: Feedback
        UI-->>User: Display Review
    and Cover Letter
        UI->>Agent: write_cover_letter(details)
        Agent->>OpenRouter: API Call
        OpenRouter-->>Agent: Cover Letter
        Agent-->>UI: Generated Letter
        UI-->>User: Display & Download
    and Interview Prep
        UI->>QC: get_questions_by_role()
        QC->>QC: Check Cache
        QC-->>UI: Questions List
        UI->>Agent: get_questions_with_tips()
        Agent->>OpenRouter: API Call
        OpenRouter-->>Agent: Tips & Coaching
        Agent-->>UI: Complete Guide
        UI-->>User: Display Questions
    end
```
### 🧩 Class Diagram
```mermaid
classDiagram
    class BaseAgent {
        +string name
        +string role
        +list instructions
        +OpenAI client
        +run(prompt)
        +_create_client()
    }
    
    class ResumeReviewerAgent {
        +review(resume_text, job_title)
    }
    
    class CoverLetterWriterAgent {
        +write(resume_text, job_title, company, job_desc, tone)
    }
    
    class InterviewCoachAgent {
        +get_questions_with_tips(job_title, experience, questions)
        +get_answer_feedback(question, answer)
        +generate_questions_fallback(job_title, experience, count)
    }
    
    class InterviewQuestionCollector {
        +dict github_sources
        +dict question_cache
        +dict fallback_questions
        +load_all_questions()
        +get_questions_by_role(role, count)
        +get_total_questions_count()
    }
    
    BaseAgent <|-- ResumeReviewerAgent
    BaseAgent <|-- CoverLetterWriterAgent
    BaseAgent <|-- InterviewCoachAgent
    
    InterviewCoachAgent --> InterviewQuestionCollector : uses
```
## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (free)
- Git (optional)

### Step-by-Step Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/Navneetsingh9/AICTE-BATCH7-AI-POWERED-RESUME-JOB-ASSISTANT.git
cd AICTE-BATCH7-AI-POWERED-RESUME-JOB-ASSISTANT
```
#### 2. Create Virtual Environment
```bash
-Windows
python -m venv venv
venv\Scripts\activate

-Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Set Up Environment Variables
```bash
Create a .env file in the root directory:
OPENROUTER_API_KEY=your_api_key_here
```

## 📁 Project Structure
```text
resume-job-assistant/
│
├── 📄 app.py                      # Main application
├── 📄 config.py                   # Configuration settings
├── 📄 requirements.txt            # Dependencies
├── 📄 .env                        # Environment variables
├── 📄 .gitignore                  # Git ignore file
├── 📄 README.md                   # This file
│
├── 📁 agents/                      # AI Agents
│   ├── 📄 __init__.py
│   ├── 📄 base_agent.py           # Base agent class
│   ├── 📄 resume_reviewer.py       # Agent 1
│   ├── 📄 cover_letter_writer.py   # Agent 2
│   └── 📄 interview_coach.py       # Agent 3
│
├── 📁 utils/                        # Utilities
│   ├── 📄 __init__.py
│   ├── 📄 pdf_extractor.py         # PDF processing
│   └── 📄 question_collector.py    # Interview questions
│
└── 📁 ui/                           # UI Components
    ├── 📄 __init__.py
    ├── 📄 styles.py                 # Custom CSS
    ├── 📄 sidebar.py                # Sidebar UI
    └── 📁 tabs/                      # Tab components
        ├── 📄 __init__.py
        ├── 📄 resume_tab.py          # Tab 1 UI
        ├── 📄 cover_letter_tab.py    # Tab 2 UI
        └── 📄 interview_tab.py       # Tab 3 UI
```

Run this test to ensure everything works:
```bash
python -c "from utils.question_collector import InterviewQuestionCollector; q = InterviewQuestionCollector(); print(f'✅ Questions loaded: {q.get_total_questions_count()}')"
```
MIT License

Copyright (c) 2026 Navneet Singh

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files...

<div align="center"> <h3>Made with ❤️ for job seekers everywhere</h3> <p>Happy Job Hunting! 🎉</p> </div> 
