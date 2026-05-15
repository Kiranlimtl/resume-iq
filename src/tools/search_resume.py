from similarity import similarity_scores

search_resume_declaration = {
    "name": "search_resume",
    "description": "Searches the resume for top 3 most relevant sections based on the job description and returns the top 3 most relevant sections.",
    "parameters": {
        "type": "object",
        "properties": {
            "job_desc": {
                "type": "string", 
                "description": "The job description used to search the resume."
            }
        },
        "required": ["job_desc"]
    }
}

def search_resume(job_desc):
    return similarity_scores(job_desc)