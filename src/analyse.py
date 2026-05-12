from google import genai
import os
from dotenv import load_dotenv
from compare import similarity_scores

load_dotenv()

content, job_desc = similarity_scores()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_analysis(content, job_desc):
    analysis = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=f"""I want you to analyse the resume base on the given sections and compare 
        it to the job description. I want a matchign score, missing keywords, rewrite suggestions, and
        even action plan to improve the resume. I want you to be critical and honest in your analysis.
        Here are the sections: {content} and here is the job description: {job_desc}""",
    )
    return analysis.text

print(generate_analysis(content, job_desc))