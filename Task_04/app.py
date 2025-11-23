import streamlit as st
from pypdf import PdfReader
import os
import json
from openai import AsyncOpenAI
from agents import Runner, set_default_openai_client, set_default_openai_api
from agent import summarizer_agent, quiz_creator_agent
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration for Gemini API ---
# Configure the client to use the Gemini API endpoint.
# The user must set these environment variables in the .env file.
gemini_api_base = "https://generativelanguage.googleapis.com/v1beta/openai/"
gemini_api_key = os.getenv("GEMINI_API_KEY")

if gemini_api_base and gemini_api_key:
    try:
        custom_client = AsyncOpenAI(base_url=gemini_api_base, api_key=gemini_api_key)
        set_default_openai_client(custom_client)
        # Set the API to chat completions, which is standard for most OpenAI-compatible APIs
        set_default_openai_api("chat_completions")
    except Exception as e:
        st.error(f"Failed to configure the API client: {e}")
else:
    st.error("Please set the GEMINI_API_BASE and GEMINI_API_KEY environment variables in your .env file.")


st.set_page_config(page_title="PDF Study Agent", page_icon="🧠", layout="wide")

st.title("🧠 PDF Study Agent")
st.write("Upload a PDF, and the agent will summarize it and create a quiz for you.")

# --- Session State Initialization ---
if 'summary' not in st.session_state:
    st.session_state.summary = ""
if 'quiz' not in st.session_state:
    st.session_state.quiz = None
if 'full_text' not in st.session_state:
    st.session_state.full_text = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""
if 'processed_file_name' not in st.session_state:
    st.session_state.processed_file_name = None

# --- Helper Functions ---
def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.session_state.error_message = f"Error extracting text from PDF: {e}"
        return None

def parse_quiz_json(quiz_json_str):
    """Parses the JSON string from the agent into a Python list of questions."""
    try:
        # The model sometimes returns the JSON wrapped in markdown
        if quiz_json_str.strip().startswith("```json"):
            quiz_json_str = quiz_json_str.strip()[7:-4]

        quiz_data = json.loads(quiz_json_str)
        return quiz_data.get("questions", [])
    except (json.JSONDecodeError, AttributeError) as e:
        st.session_state.error_message = f"Error parsing quiz data: {e}. Raw data from agent: {quiz_json_str}"
        return None

# --- UI Components ---
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and uploaded_file.name != st.session_state.processed_file_name:
    # Reset state for the new file
    st.session_state.summary = ""
    st.session_state.quiz = None
    st.session_state.full_text = ""
    st.session_state.error_message = ""
    st.session_state.user_answers = {}
    st.session_state.quiz_checked = False
    st.session_state.processed_file_name = uploaded_file.name

    with st.spinner("Extracting text from PDF..."):
        full_text = extract_text_from_pdf(uploaded_file)

    if full_text:
        st.session_state.full_text = full_text
        st.success("PDF processed successfully!")

        with st.spinner("Asking the Summarizer Agent to generate a summary..."):
            try:
                result = Runner.run_sync(summarizer_agent, st.session_state.full_text)
                summary = result.final_output
                if summary:
                    st.session_state.summary = summary
                else:
                    st.error("The Summarizer Agent failed to generate a summary.")
            except Exception as e:
                st.error(f"An error occurred with the Summarizer Agent: {e}")
    else:
        st.error(st.session_state.error_message)

# --- Display Summary ---
if st.session_state.summary:
    st.subheader("Summary")
    summary_style = st.selectbox(
        "Choose a display style for the summary:",
        ("Card", "Block", "Container", "Expander"),
        key="summary_style"
    )

    if summary_style == "Card":
        st.info(st.session_state.summary)
    elif summary_style == "Block":
        st.text_area("", st.session_state.summary, height=200)
    elif summary_style == "Container":
        with st.container():
            st.write(st.session_state.summary)
    elif summary_style == "Expander":
        with st.expander("Click to see summary", expanded=True):
            st.write(st.session_state.summary)

    if st.button("Create Quiz"):
        with st.spinner("Asking the Quiz Creator Agent to generate a quiz..."):
            try:
                result = Runner.run_sync(quiz_creator_agent, st.session_state.full_text)
                quiz_text = result.final_output
                if quiz_text:
                    quiz_questions = parse_quiz_json(quiz_text)
                    if quiz_questions:
                        st.session_state.quiz = quiz_questions
                        st.session_state.user_answers = {}
                        st.session_state.quiz_checked = False
                        st.success("Quiz created!")
                    else:
                        # Error message is set within parse_quiz_json
                        st.error(st.session_state.error_message)
                else:
                    st.error("The Quiz Creator Agent failed to generate a quiz.")
            except Exception as e:
                st.error(f"An error occurred with the Quiz Creator Agent: {e}")

# --- Display Interactive Quiz ---
if st.session_state.quiz:
    st.subheader("Quiz Time!")
    st.write("Test your knowledge based on the document.")

    for i, q in enumerate(st.session_state.quiz):
        st.markdown(f"**Question {i+1}: {q['question']}**")
        
        q_type = q.get("type")
        if q_type == "MCQ":
            options = q.get("options", [])
            answer = st.radio("Your answer:", options, key=f"q_{i}")
            st.session_state.user_answers[i] = answer
        elif q_type == "T/F":
            answer = st.radio("Your answer:", ["True", "False"], key=f"q_{i}")
            st.session_state.user_answers[i] = answer
        elif q_type == "FIB":
            answer = st.text_input("Your answer:", key=f"q_{i}")
            st.session_state.user_answers[i] = answer

    if st.button("Check Answers"):
        st.session_state.quiz_checked = True

    if st.session_state.get('quiz_checked', False):
        score = 0
        st.subheader("Results")
        for i, q in enumerate(st.session_state.quiz):
            user_answer = st.session_state.user_answers.get(i)
            correct_answer = q.get("answer")
            
            if user_answer is not None and correct_answer is not None:
                is_correct = str(user_answer).strip().lower() == str(correct_answer).strip().lower()
                if is_correct:
                    score += 1
                    st.success(f"**Question {i+1}: Correct!**")
                else:
                    st.error(f"**Question {i+1}: Incorrect.**")
                    st.info(f"Your answer: {user_answer}")
                    st.info(f"Correct answer: {correct_answer}")
            else:
                st.warning(f"**Question {i+1}: Could not determine the result.**")

        st.subheader(f"Your final score: {score}/{len(st.session_state.quiz)}")

# --- Error Display ---
if st.session_state.error_message and not st.session_state.quiz: # Avoid showing parsing errors if quiz is displayed
    st.error(st.session_state.error_message)

st.sidebar.header("About")
st.sidebar.info(
    "This is the PDF_Study_Agent, a project using the `openai-agents` SDK. "
    "It uses specialized agents to summarize documents and create quizzes."
)
