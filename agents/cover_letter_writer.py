from agents.base_agent import BaseAgent

class CoverLetterWriterAgent(BaseAgent):
    """Agent 2: Writes customized cover letters"""
    
    def __init__(self):
        instructions = [
            "You are an expert cover letter writer.",
            "Write professional, customized cover letters.",
            "Match tone to company culture (startup vs corporate).",
            "Highlight relevant skills and experiences.",
            "Show enthusiasm and fit for the role.",
            "Keep it to 3-4 paragraphs maximum.",
            "Include placeholders in [brackets] for personalization.",
            "Format with: DATE, COMPANY INFO, GREETING, BODY, CLOSING."
        ]
        super().__init__("Cover Letter Writer", "Write customized cover letters", instructions)
    
    def write(self, resume_text, job_title, company_name, job_description, tone="professional"):
        """Write a cover letter"""
        prompt = (
            f"Write a {tone} cover letter for:\n"
            f"Job Title: {job_title}\n"
            f"Company: {company_name}\n"
            f"Job Description: {job_description}\n\n"
            f"Based on this resume:\n{resume_text[:5000]}\n\n"
            f"Make it specific, enthusiastic, and tailored to the role."
        )
        return self.run(prompt)