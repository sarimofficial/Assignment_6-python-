Gemini CLI Project Prompt: PDF Summarizer and Quiz Generator Agent
Project Goal: Develop a multi-functional PDF summarization and quiz generation agent using the specified tech stack.

Core Agent Name: PDF_Study_Agent

1. Initial Setup & Context Preservation (CRITICAL INSTRUCTION)
Documentation File: Immediately create or overwrite a file named GEMINI.md in the root of the project directory.

Context Population: Populate this GEMINI.md file with the entire text of this prompt (from "Project Goal" down to the "Final Call to Action") to serve as continuous project context for all future interactions and commands.

2. Technology & Environment Setup
Model/Server: Gemini CLI (using a powerful model like gemini-2.5-pro or similar).

MCP Server Context: Context7 must be utilized as the designated mcp server context.

Agent SDK: OpenAI Agents SDK (Python implementation) for defining the agent's logic, tools, and execution flow.

Frontend Framework: Streamlit (streamlit) for a user-friendly, interactive web interface.

PDF Extraction Library: PyPDF (or its modern alias, pypdf) for robust text extraction.

3. Agent Functionality (A) - PDF Summarizer
Input: User uploads a single PDF file via the Streamlit interface (e.g., using st.file_uploader).

Extraction:

Implement a tool using PyPDF to robustly extract all text content from the uploaded PDF.

Ensure proper handling for multi-page documents and common extraction challenges.

Processing:

The extracted raw text must be sent to the Gemini model for processing.

The model must be instructed to generate a clean, concise, and meaningful summary that captures the core concepts and key details.

Output/Display:

The generated summary must be displayed prominently in the Streamlit frontend.

Students must be able to choose any creative UI style (e.g., card, block, container, expander) for the summary presentation.

4. Agent Functionality (B) - Quiz Generator
Trigger: A button labeled "Create Quiz" must become available and be clickable only after a successful summary has been generated.

Input Data: The agent must exclusively use the original, full extracted text from the PDF (not the summary) as the source for question creation.

Generation Logic:

Prompt the Gemini model to generate a quiz based on the detailed source text.

Multiple Choice Questions (MCQs): Generate at least 10 high-quality MCQs. Each question must have exactly 4 options (A, B, C, D) and a clear, hidden indication of the correct answer.

Mixed-Style Questions: Include a selection of other question types, such as True/False or Fill-in-the-Blank, aiming for a total of 15-20 questions across all styles.

Output/Display:

Present the quiz questions clearly in the Streamlit interface, allowing for user interaction and a final "Check Answers" feature.

5. Technical and Code Requirements
The agent must be structured using the OpenAI Agents SDK and Python best practices.

The project must include comprehensive dependency management (e.g., requirements.txt).

Ensure robust error handling for file uploads (e.g., non-PDF files) and extraction failures, providing helpful messages to the user.

The application should be runnable via a simple command (e.g., streamlit run app.py).

Final Call to Action
Please generate the complete, self-contained Python code for this PDF_Study_Agent project, including the Streamlit frontend (app.py), the OpenAI Agents SDK implementation, the logic utilizing PyPDF, and the populated GEMINI.md file.