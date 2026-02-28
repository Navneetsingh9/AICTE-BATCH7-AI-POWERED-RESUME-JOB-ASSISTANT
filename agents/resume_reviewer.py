from agents.base_agent import BaseAgent

class ResumeReviewerAgent(BaseAgent):
    """Agent 1: Reviews resumes and suggests improvements"""
    
    def __init__(self):
        instructions = [
            "You are an expert resume reviewer and career coach.",
            "Review resumes professionally and provide constructive feedback.",
            "Focus on: formatting, content, achievements, keywords, and impact.",
            "Suggest specific improvements with examples.",
            "Highlight strengths and areas for improvement.",
            "Check for ATS (Applicant Tracking System) friendliness.",
            "Format response with: STRENGTHS, AREAS TO IMPROVE, SPECIFIC SUGGESTIONS, KEYWORDS TO ADD."
        ]
        super().__init__("Resume Reviewer", "Review resumes and suggest improvements", instructions)
    
    def review(self, resume_text, job_title=None):
        """Review a resume"""
        job_context = f" for a {job_title} position" if job_title else ""
        prompt = f"Please review this resume{job_context}:\n\n{resume_text[:8000]}\n\nProvide specific, actionable feedback to improve it."
        return self.run(prompt)