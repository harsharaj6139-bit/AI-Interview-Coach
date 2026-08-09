import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from pypdf import PdfReader
from docx import Document
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY not found in .env file")
    st.stop()

client = genai.Client(api_key=API_KEY)
# Page configuration
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)

# Initialize session state
if "role" not in st.session_state:
    st.session_state.role = "Python Developer"

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Intermediate"

if "interview_type" not in st.session_state:
    st.session_state.interview_type = "Mixed"

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

if "evaluation_history" not in st.session_state:
    st.session_state.evaluation_history = []

if "active_page" not in st.session_state:
    st.session_state.active_page = "interview"


# Sidebar
with st.sidebar:
# Sidebar#
 with st.sidebar:

    st.markdown(
        """
        <div style="
            font-size:28px;
            font-weight:800;
            margin-bottom:5px;
        ">
            🎤 Interview Coach
        </div>

        <div style="
            color:#94A3B8;
            font-size:13px;
            margin-bottom:25px;
        ">
            AI Career Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### 🧭 WORKSPACE")

    sidebar_page = st.radio(
        "Navigate",
        [
            "🎤 Interview",
            "📊 Dashboard",
            "💡 Improvement Tips"
        ],
        label_visibility="collapsed"
    )
if sidebar_page == "🎤 Interview":
    st.session_state.active_page = "interview"

elif sidebar_page == "📊 Dashboard":
    st.session_state.active_page = "dashboard"

elif sidebar_page == "💡 Improvement Tips":
    st.session_state.active_page = "tips"
    st.markdown("---")

    st.markdown("### 🤖 AI ENGINE")

    st.success("● Gemini Connected")

    st.markdown("---")

    st.caption("AI Interview Coach v1.0")
# Custom CSS
st.markdown("""
<style>

.stApp {
    background-color: #0B0F14;
    color: #F8FAFC;
}

.main-title {
    font-size: 52px;
    font-weight: 800;
    text-align: center;
    margin-top: 40px;
}

.subtitle {
    text-align: center;
    color: #94A3B8;
    font-size: 19px;
    margin-bottom: 40px;
}

.card {
    background-color: #11161D;
    border: 1px solid #252C35;
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 20px;
}

.card h3 {
    color: #F8FAFC;
}

.card p {
    color: #94A3B8;
    line-height: 1.6;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    padding: 12px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# Header
st.markdown(
    '<div class="main-title">🎤 AI Interview Coach</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Practice smarter. Answer confidently. Get AI-powered interview feedback.'
    '</div>',
    unsafe_allow_html=True
)


# Features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card">
        <h3>🧠 AI Questions</h3>
        <p>
        Generate technical and HR interview questions
        based on your target job role.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h3>📊 Answer Evaluation</h3>
        <p>
        Get AI-powered feedback and a score
        for every interview answer.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <h3>🎯 Skill Improvement</h3>
        <p>
        Identify weak areas and receive
        personalized improvement suggestions.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Resume Upload
st.markdown("---")

st.markdown("## 📄 Upload Your Resume")

resume = st.file_uploader(
    "Upload your resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

if resume:
    st.success(f"✅ {resume.name} uploaded successfully!")

    try:
        # Extract resume text
        if resume.name.lower().endswith(".pdf"):
            reader = PdfReader(resume)
            resume_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text + "\n"

        elif resume.name.lower().endswith(".docx"):
            document = Document(resume)
            resume_text = "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            )

        # Save resume text for the interview
        st.session_state.resume_text = resume_text

        if resume_text.strip():
            st.success("📄 Resume text extracted successfully!")
        else:
            st.warning("⚠️ Resume uploaded, but no text could be extracted.")

    except Exception as e:
        st.error(f"❌ Could not read resume: {e}")
# Interview setup
if st.session_state.get("active_page", "interview") == "interview":

    st.markdown("## 🚀 Start Your Interview")

col1, col2 = st.columns(2)

with col1:
    role = st.selectbox(
        "Select your target role",
        [
            "Python Developer",
            "Software Engineer",
            "Data Analyst",
            "Web Developer",
            "Machine Learning Engineer",
            "AI Engineer"
        ]
    )

with col2:
    difficulty = st.selectbox(
        "Select difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


# Interview type
interview_type = st.radio(
    "Interview Type",
    [
        "Technical",
        "HR",
        "Mixed"
    ],
    horizontal=True
)


# Start button
if st.button("🎤 Start Interview"):

    st.session_state.interview_started = True
    st.session_state.role = role
    st.session_state.difficulty = difficulty
    st.session_state.interview_type = interview_type

resume_text = st.session_state.get(
    "resume_text",
    "No resume uploaded."
)

prompt = f"""
You are an expert interviewer.

Generate ONE personalized interview question.

Candidate Information:
Target Role: {role}
Difficulty: {difficulty}
Interview Type: {interview_type}

Candidate Resume:
{resume_text[:12000]}

Rules:
- Ask exactly ONE question.
- Use information from the candidate's resume when relevant.
- The question should be realistic for an actual interview.
- Do not provide the answer.
- Do not invent experience that is not present in the resume.
- Keep the question clear and concise.
"""

try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        st.session_state.current_question = response.text

except Exception as e:
        st.error(f"❌ Gemini API error: {e}")


# Display question
if "current_question" in st.session_state:

    st.markdown("---")

    # Initialize interview tracking
    if "question_number" not in st.session_state:
        st.session_state.question_number = 1

    if "total_score" not in st.session_state:
        st.session_state.total_score = 0

    if "answered_questions" not in st.session_state:
        st.session_state.answered_questions = 0

    # Progress
    st.markdown(
        f"### Question {st.session_state.question_number} / 5"
    )

    progress = min(st.session_state.question_number / 5, 1.0)
    st.progress(progress)

    # Question
    st.markdown("## 🎤 Interview Question")

    st.info(st.session_state.current_question)

    # Answer
    answer = st.text_area(
        "💬 Your Answer",
        placeholder="Type your answer here...",
        key=f"answer_{st.session_state.question_number}"
    )

    col1, col2 = st.columns(2)

    # Evaluate
    with col1:

        if st.button("📊 Evaluate Answer"):

            if not answer.strip():

                st.warning("Please enter your answer first.")

            else:

                evaluation_prompt = f"""
You are an expert interviewer.

Target Role: {st.session_state.role}
Difficulty: {st.session_state.difficulty}
Interview Type: {st.session_state.interview_type}

Question:
{st.session_state.current_question}

Candidate Answer:
{answer}

Evaluate the candidate.

Return your response in exactly this structure:

SCORE: X/10

STRENGTHS:
- point 1
- point 2

IMPROVEMENTS:
- point 1
- point 2

SAMPLE ANSWER:
Give a concise improved answer.

SKILLS:
- skill 1
- skill 2
"""

                try:

                    evaluation = client.models.generate_content(
                        model="gemini-3.5-flash-lite",
                        contents=evaluation_prompt
                    )

                    evaluation_text = evaluation.text

                    st.session_state.last_evaluation = evaluation_text
                    st.session_state.last_evaluation = evaluation_text

                    if "evaluation_history" not in st.session_state:
                        st.session_state.evaluation_history = []

                    st.session_state.evaluation_history.append({
                        "question": st.session_state.current_question,
                        "evaluation": evaluation_text
                    })
                    # Extract score
                    import re

                    score_match = re.search(
                        r"SCORE:\s*(\d+)\s*/\s*10",
                        evaluation_text,
                        re.IGNORECASE
                    )

                    if score_match:

                        score = int(score_match.group(1))

                        st.session_state.total_score += score

                        st.session_state.answered_questions += 1

                    st.markdown("---")

                    st.markdown("## 📊 AI Evaluation")

                    st.markdown(evaluation_text)

                except Exception as e:

                    st.error(
                        f"❌ Evaluation failed: {e}"
                    )

    # Next question
with col2:
    if st.button("➡️ Next Question"):

        # Stop after 5 questions
        if st.session_state.question_number >= 5:
            st.session_state.interview_finished = True
            st.rerun()

        resume_text = st.session_state.get(
            "resume_text",
            "No resume uploaded."
        )

        next_question_prompt = f"""
You are conducting a professional interview.

Target Role: {st.session_state.role}
Difficulty: {st.session_state.difficulty}
Interview Type: {st.session_state.interview_type}

Candidate Resume:
{resume_text[:12000]}

Previous Question:
{st.session_state.current_question}

Generate the NEXT interview question.

Rules:
- Ask exactly ONE question.
- Do not repeat the previous question.
- Use the candidate's resume when appropriate.
- Cover different areas of the candidate's skills, projects, education, or experience.
- Make it realistic for the selected role.
- Do not invent information.
- Do not provide the answer.
"""

        try:
            next_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=next_question_prompt
            )

            # Only increase if we are still below 5
            if st.session_state.question_number < 5:
                st.session_state.question_number += 1
                st.session_state.current_question = next_response.text

            st.rerun()

        except Exception as e:
            st.error(
                f"❌ Could not generate next question: {e}"
            )

# Interview completed
if st.session_state.get("interview_finished", False):

    st.markdown("---")

    st.markdown("# 🏆 Interview Dashboard")
    st.markdown("## 🤖 AI Career Assessment")
    answered = st.session_state.get("answered_questions", 0)
    total = st.session_state.get("total_score", 0)

    if answered > 0:

        average = total / answered
        # Generate final AI assessment
        resume_text = st.session_state.get(
            "resume_text",
            "No resume uploaded."
        )

        history_text = ""

        for index, item in enumerate(
            st.session_state.get("evaluation_history", []),
            start=1
        ):
            history_text += f"""
Question {index}:
{item["question"]}

Evaluation:
{item["evaluation"]}

---
"""

        final_prompt = f"""
You are a professional interview coach.

Analyze the candidate's complete interview performance.

Target Role:
{st.session_state.role}

Difficulty:
{st.session_state.difficulty}

Interview Type:
{st.session_state.interview_type}

Average Interview Score:
{average:.1f}/10

Candidate Resume:
{resume_text[:12000]}

Interview History:
{history_text[:12000]}

Create a concise final career assessment.

Use exactly these sections:

OVERALL ASSESSMENT
Give a short summary of the candidate's interview performance.

STRENGTHS
- List the candidate's strongest areas.

WEAKNESSES
- List the most important areas to improve.

RECOMMENDED SKILLS
- List skills the candidate should strengthen.

HIRING READINESS
Give one rating:
Excellent / Good / Developing / Needs Improvement

IMPROVEMENT PLAN
Give 3 practical steps the candidate should take next.

Rules:
- Base the assessment on the resume and interview performance.
- Do not invent experience.
- Be honest and constructive.
"""

        try:

            final_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=final_prompt
            )

            final_report = final_response.text

            st.session_state.final_report = final_report

        except Exception as e:

            st.error(
                f"❌ Could not generate final assessment: {e}"
            )
        if "final_report" in st.session_state:

            st.markdown("---")

            st.markdown("## 📋 Final AI Interview Report")

            st.markdown(
                st.session_state.final_report
            )
        # Performance level
        if average >= 8:
            level = "🌟 Excellent"
        elif average >= 6:
            level = "👍 Good"
        elif average >= 4:
            level = "📈 Needs Improvement"
        else:
            level = "💪 Keep Practicing"

        # Score cards
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "Overall Score",
                f"{average:.1f}/10"
            )

        with col2:
            st.metric(
                "Questions",
                answered
            )

        with col3:
            st.metric(
                "Total Points",
                f"{total}/10"
            )

        with col4:
            st.metric(
                "Performance",
                level
            )

        st.markdown("---")

        # Progress
        st.markdown("## 📊 Overall Performance")

        st.progress(min(average / 10, 1.0))

        if average >= 8:
            st.success(
                "Excellent! Your answers demonstrate strong interview readiness."
            )

        elif average >= 6:
            st.info(
                "Good performance. Continue practicing to become more confident."
            )

        else:
            st.warning(
                "Keep practicing. Focus on explaining your answers clearly."
            )

        # Evaluation history
        if "evaluation_history" in st.session_state:

            st.markdown("---")

            st.markdown("## 📝 Question-by-Question Review")

            for index, item in enumerate(
                st.session_state.evaluation_history,
                start=1
            ):

                with st.expander(
                    f"Question {index}"
                ):

                    st.markdown("### 🎤 Question")

                    st.write(item["question"])

                    st.markdown("### 🤖 AI Evaluation")

                    st.markdown(item["evaluation"])

        st.markdown("---")

        st.markdown("## 🎯 Career Recommendation")

        if average >= 8:

            st.success(
                "You appear well prepared for this interview level. "
                "Focus on real-world projects and advanced questions."
            )

        elif average >= 6:

            st.info(
                "You have a good foundation. "
                "Practice more technical explanations and real-world scenarios."
            )

        else:

            st.warning(
                "More preparation is recommended. "
                "Strengthen your fundamentals and practice answering questions aloud."
            )

    else:

        st.warning(
            "No answers were evaluated. Complete an interview to see your dashboard."
        )

    st.markdown("---")

    if st.button("🔄 Start New Interview"):

        keys_to_clear = [
            "current_question",
            "question_number",
            "total_score",
            "answered_questions",
            "interview_finished",
            "last_evaluation",
            "evaluation_history"
        ]

        for key in keys_to_clear:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()