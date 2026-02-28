# utils/question_collector.py
import requests
import random
import streamlit as st
import time
import json

class InterviewQuestionCollector:
    """Collects real interview questions from multiple free sources with fallback"""
    
    def __init__(self):
        # UPDATED: Working GitHub URLs
        self.github_sources = [
            {
                "name": "Tech Interview Handbook",
                # The handbook now uses a different structure
                "url": "https://raw.githubusercontent.com/yangshun/tech-interview-handbook/main/README.md",
                "type": "general",
                "parser": "simple"  # Different parsing needed
            },
            {
                "name": "JavaScript Questions",
                "url": "https://raw.githubusercontent.com/lydiahallie/javascript-questions/master/README.md",  # It's a README, not JSON!
                "type": "javascript",
                "parser": "markdown"
            },
            {
                "name": "Backend Interview Questions",
                "url": "https://raw.githubusercontent.com/arialdomartini/Back-End-Developer-Interview-Questions/master/README.md",  # It's a README
                "type": "backend",
                "parser": "markdown"
            },
            {
                "name": "System Design Primer",
                "url": "https://raw.githubusercontent.com/donnemartin/system-design-primer/master/README.md",  # It's a README
                "type": "system-design",
                "parser": "markdown"
            },
            {
                "name": "Python Interview Questions",
                # Alternative source for Python questions
                "url": "https://raw.githubusercontent.com/learning-zone/python-interview-questions/master/questions.md",
                "type": "python",
                "parser": "markdown"
            }
        ]
        
        # Built-in fallback questions (in case APIs fail)
        self.fallback_questions = {
            "general": [
                {"question": "Tell me about yourself.", "source": "Built-in", "difficulty": "easy"},
                {"question": "Why do you want to work here?", "source": "Built-in", "difficulty": "easy"},
                {"question": "What are your greatest strengths?", "source": "Built-in", "difficulty": "easy"},
                {"question": "What are your weaknesses?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Where do you see yourself in 5 years?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Why are you leaving your current job?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Tell me about a time you faced a challenge.", "source": "Built-in", "difficulty": "hard"},
            ],
            "frontend": [
                {"question": "What's the difference between == and === in JavaScript?", "source": "Built-in", "difficulty": "easy"},
                {"question": "Explain the box model in CSS.", "source": "Built-in", "difficulty": "easy"},
                {"question": "What is the virtual DOM in React?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain closures in JavaScript.", "source": "Built-in", "difficulty": "medium"},
                {"question": "What's the difference between let, const, and var?", "source": "Built-in", "difficulty": "easy"},
                {"question": "What is event delegation?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain the 'this' keyword in JavaScript.", "source": "Built-in", "difficulty": "hard"},
            ],
            "backend": [
                {"question": "What is RESTful API design?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain the difference between SQL and NoSQL databases.", "source": "Built-in", "difficulty": "medium"},
                {"question": "What is caching and why is it important?", "source": "Built-in", "difficulty": "medium"},
                {"question": "How would you design a scalable system?", "source": "Built-in", "difficulty": "hard"},
                {"question": "What is load balancing?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain ACID properties in databases.", "source": "Built-in", "difficulty": "hard"},
                {"question": "What is database indexing and how does it work?", "source": "Built-in", "difficulty": "medium"},
            ],
            "python": [
                {"question": "What are Python decorators?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain list comprehensions in Python.", "source": "Built-in", "difficulty": "easy"},
                {"question": "What's the difference between a tuple and a list?", "source": "Built-in", "difficulty": "easy"},
                {"question": "How does memory management work in Python?", "source": "Built-in", "difficulty": "hard"},
                {"question": "What are Python generators?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain the Global Interpreter Lock (GIL).", "source": "Built-in", "difficulty": "hard"},
            ],
            "javascript": [
                {"question": "Explain event delegation in JavaScript.", "source": "Built-in", "difficulty": "medium"},
                {"question": "What is a promise in JavaScript?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain the 'this' keyword in JavaScript.", "source": "Built-in", "difficulty": "hard"},
                {"question": "What is hoisting in JavaScript?", "source": "Built-in", "difficulty": "medium"},
                {"question": "Explain async/await in JavaScript.", "source": "Built-in", "difficulty": "medium"},
                {"question": "What are closures and how do they work?", "source": "Built-in", "difficulty": "hard"},
            ],
            "system-design": [
                {"question": "Design a URL shortening service like TinyURL.", "source": "Built-in", "difficulty": "hard"},
                {"question": "How would you design Twitter's backend?", "source": "Built-in", "difficulty": "hard"},
                {"question": "Design a messaging system like WhatsApp.", "source": "Built-in", "difficulty": "hard"},
                {"question": "How would you scale a database?", "source": "Built-in", "difficulty": "hard"},
                {"question": "Design a recommendation system.", "source": "Built-in", "difficulty": "hard"},
                {"question": "How would you design a chat system?", "source": "Built-in", "difficulty": "hard"},
            ]
        }
        
        self.question_cache = {}
        self._load_fallback_questions()  # Load fallbacks immediately
        
        # Try to load from GitHub in background (but don't wait)
        import threading
        thread = threading.Thread(target=self.load_all_questions)
        thread.daemon = True
        thread.start()
    
    def load_all_questions(self):
        """Load questions from all sources with timeout and error handling"""
        successful_loads = 0
        
        for source in self.github_sources:
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(source["url"], timeout=2, headers=headers)
                
                if response.status_code == 200:
                    if source.get("parser") == "markdown":
                        # Parse markdown to extract questions (simplified)
                        questions = self._parse_markdown_questions(response.text, source["name"], source["type"])
                        if source["type"] not in self.question_cache:
                            self.question_cache[source["type"]] = []
                        self.question_cache[source["type"]].extend(questions)
                        successful_loads += len(questions)
                    else:
                        # Try JSON parsing
                        try:
                            data = response.json()
                            if source["type"] not in self.question_cache:
                                self.question_cache[source["type"]] = []
                            
                            if isinstance(data, list):
                                for item in data:
                                    if isinstance(item, dict):
                                        question = {
                                            "question": item.get("question", item.get("title", "")),
                                            "answer": item.get("answer", item.get("explanation", "")),
                                            "source": source["name"],
                                            "type": source["type"],
                                            "difficulty": item.get("difficulty", "medium")
                                        }
                                        if question["question"]:
                                            self.question_cache[source["type"]].append(question)
                                            successful_loads += 1
                        except json.JSONDecodeError:
                            pass
                else:
                    print(f"Failed to load {source['name']}: HTTP {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"Timeout loading {source['name']}")
            except Exception as e:
                print(f"Error loading {source['name']}: {str(e)}")
        
        if successful_loads == 0:
            print("No questions loaded from internet. Using built-in fallback questions.")
    
    def _parse_markdown_questions(self, text, source_name, q_type):
        """Simple markdown parser to extract questions"""
        questions = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            # Look for lines that look like questions (start with number, dash, or contain '?')
            if (line and len(line) > 10 and len(line) < 200 and 
                ('?' in line or line[0].isdigit() or line.startswith('-') or line.startswith('*'))):
                
                # Clean up the line
                question_text = line.lstrip('0123456789.-* ').strip()
                if question_text and len(question_text) > 10:
                    questions.append({
                        "question": question_text,
                        "answer": "Check online resources for detailed answer",
                        "source": source_name,
                        "type": q_type,
                        "difficulty": "medium"
                    })
        
        return questions[:20]  # Limit to first 20
    
    def _load_fallback_questions(self):
        """Load built-in fallback questions"""
        for q_type, questions in self.fallback_questions.items():
            if q_type not in self.question_cache:
                self.question_cache[q_type] = []
            self.question_cache[q_type].extend(questions)
    
    def get_questions_by_role(self, role: str, count: int = 10) -> list:
        """Get questions relevant to a specific role"""
        
        role_lower = role.lower()
        relevant_types = []
        
        # Map roles to question types
        if any(word in role_lower for word in ["frontend", "front-end", "react", "vue", "angular", "ui", "css"]):
            relevant_types = ["frontend", "javascript", "general"]
        elif any(word in role_lower for word in ["backend", "back-end", "api", "server", "database"]):
            relevant_types = ["backend", "python", "system-design", "general"]
        elif any(word in role_lower for word in ["fullstack", "full-stack", "web"]):
            relevant_types = ["frontend", "backend", "javascript", "python", "general"]
        elif any(word in role_lower for word in ["python", "django", "flask"]):
            relevant_types = ["python", "backend", "general"]
        elif any(word in role_lower for word in ["javascript", "js", "node", "nodejs"]):
            relevant_types = ["javascript", "frontend", "general"]
        elif any(word in role_lower for word in ["system design", "architecture", "scalable"]):
            relevant_types = ["system-design", "backend", "general"]
        elif any(word in role_lower for word in ["data", "scientist", "analyst", "ml", "ai"]):
            relevant_types = ["python", "general"]
        else:
            relevant_types = ["general", "frontend", "backend", "javascript"]
        
        # Collect questions
        all_questions = []
        seen_questions = set()
        
        for q_type in relevant_types:
            if q_type in self.question_cache:
                for q in self.question_cache[q_type]:
                    if q['question'] not in seen_questions:
                        all_questions.append(q)
                        seen_questions.add(q['question'])
        
        # Shuffle and return requested count
        random.shuffle(all_questions)
        return all_questions[:min(count, len(all_questions))]
    
    def get_total_questions_count(self):
        """Get total number of questions in cache"""
        total = 0
        for q_list in self.question_cache.values():
            total += len(q_list)
        return total