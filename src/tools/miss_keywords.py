from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

get_missing_keywords_declaration = {
    "name": "get_missing_keywords",
    "description": "Identifies missing keywords in the most similar sections of the resume compared to the job description.",
    "parameters": {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "..."
            },
            "job_desc": {
                "type": "string", 
                "description": "..."
            }
        },
        "required": ["content", "job_desc"]
    }
}

def get_missing_keywords(content, job_desc):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"Given this resume: {content} and this job description: {job_desc}, list all keywords and skills in the job description that are missing from the resume."
    )
    return response.text