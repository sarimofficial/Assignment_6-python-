from agents import Agent

# This agent is specialized in summarizing text, using a Gemini model via a custom endpoint.
summarizer_agent = Agent(
    name="Summarizer",
    instructions="You are an expert in summarizing texts. Summarize the given text concisely and accurately.",
    model="gemini-2.5-flash"
)

# This agent is specialized in creating quizzes in a specific JSON format, using a Gemini model via a custom endpoint.
quiz_creator_agent = Agent(
    name="Quiz Creator",
    instructions="""
    You are an expert in creating quizzes from text.
    Based on the provided text, generate a quiz with 15-20 questions in valid JSON format.
    The JSON object must have a single key "questions" which is an array of question objects.
    Each question object must have:
    1. "type": "MCQ", "T/F", or "FIB"
    2. "question": The question text.
    3. For "MCQ", an "options" array of exactly 4 strings.
    4. For "FIB", the blank part should be represented as "___".
    5. "answer": The correct answer. For "MCQ", this is the full text of the correct option.
    """,
    model="gemini-2.5-flash"
)