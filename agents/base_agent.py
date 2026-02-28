# agents/base_agent.py
import os
from openai import OpenAI
from dotenv import load_dotenv
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, DEFAULT_MODEL

load_dotenv()

class BaseAgent:
    
    def __init__(self, name, role, instructions):
        self.name = name
        self.role = role
        self.instructions = instructions
        self.client = self._create_client()
    
    def _create_client(self):
        """Create and configure the OpenAI client for OpenRouter"""
        return OpenAI(
            base_url=OPENROUTER_BASE_URL,
            api_key=OPENROUTER_API_KEY,
            default_headers={
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": f"AI Resume Assistant - {self.name}"
            }
        )
    
    def run(self, prompt, system_message=None):
        """Run the agent with given prompt"""
        try:
            # Use custom system message or default instructions
            system_content = system_message if system_message else "\n".join(self.instructions)
            
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,  # "openrouter/free"
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def run_with_messages(self, messages):
        """Run with a list of messages (more flexibility)"""
        try:
            response = self.client.chat.completions.create(
                model=DEFAULT_MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"