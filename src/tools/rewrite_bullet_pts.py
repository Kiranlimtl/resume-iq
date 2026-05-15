from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

rewrite_bullet_pts_declaration = {
    "name": "rewrite_bullet_pts",
    "description": "Rewrites the bullet points in the top 3 most relevanant sections of theresume to be more impactful and relevant to the job description.",
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

def rewrite_bullet_pts(content, job_desc):
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""Given this parts of the resume: {content} and this job description: {job_desc}, 
            rewrite the bullet points in the resume to be more impactful and relevant to the job description. 
            Make sure to use action verbs, quantify achievements, 
            and tailor the bullet points to highlight the most relevant skills and experiences for the job description.""",
    )
    return response.text