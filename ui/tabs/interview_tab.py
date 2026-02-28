# ui/tabs/interview_tab.py
import streamlit as st

def render_interview_tab(agent, question_collector):
    """Render the interview coach tab"""
    st.markdown('<div class="agent-card"><h3>🎤 Agent 3: Interview Coach</h3>', unsafe_allow_html=True)
    st.caption("Practice with REAL interview questions collected from the internet!")
    
    # Show source stats
    with st.expander("📚 Question Sources", expanded=False):
        total_q = question_collector.get_total_questions_count()
        st.markdown(f"""
        **Questions collected from:**
        - Tech Interview Handbook (Google, Meta, Amazon)
        - Front End Interview Handbook
        - Backend Interview Questions
        - Python Interview Questions
        - JavaScript Questions
        - System Design Primer
        
        **Total Questions in Database: {total_q}+** from real tech company interviews!
        """)
    
    mode = st.radio("Choose mode:", [
        "📋 Get Practice Questions", 
        "💬 Get Answer Feedback"
    ], horizontal=True)
    
    if mode == "📋 Get Practice Questions":
        col1, col2 = st.columns(2)
        
        with col1:
            interview_job = st.text_input("🎯 Job Title", 
                                         placeholder="e.g., Frontend Developer, Data Scientist")
            exp_level = st.selectbox("📊 Experience Level", 
                                    ["Entry", "Junior", "Mid-Level", "Senior", "Lead"])
        
        with col2:
            num_q = st.slider("🔢 Number of Questions", 5, 20, 10)
        
        if st.button("🎯 Get Real Interview Questions", type="primary", use_container_width=True):
            if interview_job:
                with st.spinner(f"Fetching real interview questions for {interview_job}..."):
                    
                    # Step 1: Get real questions from the collector
                    real_questions = question_collector.get_questions_by_role(interview_job, num_q)
                    
                    # Step 2: Check if we got any questions
                    if real_questions and len(real_questions) > 0:
                        st.success(f"✅ Found {len(real_questions)} real interview questions!")
                        
                        # Show the raw questions first (optional)
                        with st.expander("📋 View Raw Questions"):
                            for i, q in enumerate(real_questions, 1):
                                st.markdown(f"**{i}. {q['question']}**")
                                st.caption(f"Source: {q['source']} | Difficulty: {q['difficulty']}")
                                st.markdown("---")
                        
                        # Step 3: Get AI coaching tips for these questions
                        with st.spinner("🤔 AI is analyzing questions and adding tips..."):
                            coached_questions = agent.get_questions_with_tips(
                                interview_job, 
                                exp_level, 
                                real_questions
                            )
                            
                            st.markdown("### 🎯 Interview Questions with Expert Tips")
                            st.markdown(coached_questions)
                            
                            # Store in session state for later practice
                            st.session_state.last_questions = real_questions
                            st.session_state.last_job = interview_job
                    else:
                        st.warning("⚠️ No specific questions found in database. Using AI-generated questions...")
                        
                        # Fallback to AI-generated questions
                        generated = agent.generate_questions_fallback(interview_job, exp_level, num_q)
                        st.markdown("### 🎯 Generated Interview Questions")
                        st.markdown(generated)
            else:
                st.error("Please enter a job title")
    
    else:  # Answer Feedback mode
        st.markdown("#### 💬 Get feedback on your interview answers")
        
        # Option to use previous questions
        if 'last_questions' in st.session_state:
            with st.expander("📋 Use a question from last session"):
                question_options = [q['question'] for q in st.session_state.last_questions]
                selected_q = st.selectbox("Select a question:", question_options)
                if selected_q:
                    st.session_state.selected_feedback_question = selected_q
        
        question = st.text_area("❓ Interview Question", 
                               value=st.session_state.get('selected_feedback_question', ''),
                               placeholder="Paste the interview question here...", 
                               height=80)
        
        your_answer = st.text_area("✍️ Your Answer", 
                                  placeholder="Write your answer here... (Use STAR method for behavioral questions)", 
                                  height=150)
        
        if st.button("💬 Get Feedback", type="primary", use_container_width=True):
            if question and your_answer:
                with st.spinner("Analyzing your answer..."):
                    feedback = agent.get_answer_feedback(question, your_answer)
                    st.markdown("### 📊 Feedback on Your Answer")
                    st.markdown(feedback)
            else:
                st.error("Please provide both question and your answer")
        
        # STAR method guide
        with st.expander("📝 STAR Method Guide"):
            st.markdown("""
            **STAR Method for Behavioral Questions:**
            
            - **S**ituation: Set the context (where/when) - 1-2 sentences
            - **T**ask: Describe the challenge/goal - 1 sentence
            - **A**ction: Explain what YOU did - 2-3 sentences
            - **R**esult: Share the outcome with numbers - 1-2 sentences
            
            **Example:**
            > "When I was working at X (Situation), we needed to improve customer satisfaction (Task). 
            > I implemented a new feedback system and trained the team (Action). 
            > This increased satisfaction scores by 30% in 3 months (Result)."
            
            **Common Mistakes:**
            - Being too vague
            - Not mentioning YOUR specific role
            - Forgetting the result/metrics
            - Rambling without structure
            """)