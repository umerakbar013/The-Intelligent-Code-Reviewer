# Intelligent Code Reviewer & Explainer

A developer utility tool that analyzes code blocks, identifies bugs, and explains the code in plain language using AI. 

## Tech Stack
*   **Backend:** FastAPI (Python)
*   **AI SDK:** Official `google-genai` Python SDK
*   **Frontend:** Vanilla HTML, CSS (Tailwind), JavaScript
*   **Rendering:** Marked.js and Highlight.js

## Setup Instructions
1. Navigate to the `backend/` directory.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API key to `backend/.env`.
4. Run the backend: `uvicorn main:app --reload`
5. Open `frontend/index.html` in your browser.