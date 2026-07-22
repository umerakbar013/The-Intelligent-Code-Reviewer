from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Intelligent Code Reviewer API")

# Allow the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the Gemini client
# It will automatically pick up the GEMINI_API_KEY from the environment
client = genai.Client()

class CodeReviewRequest(BaseModel):
    code: str
    language: str

# System instruction to force structured Markdown output
SYSTEM_INSTRUCTION = """
You are an expert software engineer and code reviewer. 
Your objective is to analyze the provided code block, identify bugs, explain the code in plain language, and provide an optimized version.

You MUST format your output strictly in Markdown using the following structure:
### 🐛 Bug Report
(List any identified bugs, logic errors, or structural issues. If none, state that the code appears sound).

### 📖 Plain Language Explanation
(Explain what the code does clearly and concisely).

### ✨ Optimized Code
(Provide the refactored code within a markdown code block with the appropriate language tag for syntax highlighting).
"""

@app.post("/api/review")
async def review_code(request: CodeReviewRequest):
    try:
        # Construct the context window for the model
        prompt = f"Please review the following {request.language} code:\n\n```{request.language}\n{request.code}\n```"
        
        # Generate the structured response
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
            )
        )
        return {"markdown_output": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Run the server locally
    uvicorn.run(app, host="0.0.0.0", port=8000)