from agents.base_agent import BaseAgent

class InterviewCoachAgent(BaseAgent):
    """Agent 3: Provides interview coaching with real questions from QuestionCollector"""
    
    def __init__(self):
        instructions = [
            "You are an expert interview coach.",
            "You have access to real interview questions from top companies.",
            "For each question, provide tips on how to answer effectively.",
            "Use the STAR method (Situation, Task, Action, Result) for behavioral questions.",
            "Suggest what interviewers are looking for in each answer.",
            "Include common pitfalls to avoid.",
            "Be encouraging and constructive in your feedback."
        ]
        super().__init__("Interview Coach", "Practice interview questions and tips", instructions)
    
    def get_questions_with_tips(self, job_title, experience_level, questions_data):
        """
        Get interview questions with coaching tips
        questions_data should be a list of dicts with 'question', 'source', 'difficulty'
        """
        if not questions_data:
            return "No questions found for this role. Please try a different job title."
        
        # Format the questions for the prompt
        questions_text = ""
        for i, q in enumerate(questions_data, 1):
            questions_text += f"\n\n### Question {i}: {q['question']}\n"
            questions_text += f"**Source:** {q.get('source', 'Unknown')}\n"
            questions_text += f"**Difficulty:** {q.get('difficulty', 'Medium')}\n"
        
        prompt = (
            f"Job Title: {job_title}\nExperience Level: {experience_level}\n\n"
            f"Here are real interview questions collected from various sources:\n{questions_text}\n\n"
            f"For EACH question, provide:\n"
            f"1. What the interviewer is really asking\n"
            f"2. Key points to include in your answer\n"
            f"3. A sample answer structure (use STAR method for behavioral questions)\n"
            f"4. Common mistakes to avoid\n\n"
            f"Make sure each question has its own section with clear numbering."
        )
        return self.run(prompt)
    
    def get_single_question_tip(self, question_data):
        """Get tips for a single question"""
        prompt = (
            f"Question: {question_data['question']}\n"
            f"Source: {question_data.get('source', 'Unknown')}\n"
            f"Difficulty: {question_data.get('difficulty', 'Medium')}\n\n"
            f"Provide:\n"
            f"1. What the interviewer is really asking\n"
            f"2. Key points to include in your answer\n"
            f"3. A sample answer structure\n"
            f"4. Common mistakes to avoid"
        )
        return self.run(prompt)
    
    def get_answer_feedback(self, question, answer):
        """Get feedback on an interview answer"""
        prompt = (
            f"Interview Question: {question}\n\n"
            f"My Answer: {answer}\n\n"
            f"Please provide feedback on this answer:\n"
            f"1. What was good about it? (strengths)\n"
            f"2. What could be improved? (areas for growth)\n"
            f"3. Did it use the STAR method effectively (if applicable)?\n"
            f"4. Suggest a better way to structure the answer if needed.\n"
            f"5. Rate this answer: (Weak/Good/Excellent)"
        )
        return self.run(prompt)
    
    def generate_questions_fallback(self, job_title, experience_level, num_questions=10):
        """Generate interview questions when no real ones are available (fallback)"""
        prompt = (
            f"Generate {num_questions} interview questions for a {job_title} role "
            f"with {experience_level} experience level.\n\n"
            f"Include a mix of:\n"
            f"- Behavioral questions (use STAR method)\n"
            f"- Technical questions specific to {job_title}\n"
            f"- Situational questions\n"
            f"- Questions about experience and background\n\n"
            f"For each question, add a brief tip on what the interviewer is looking for."
        )
        return self.run(prompt)