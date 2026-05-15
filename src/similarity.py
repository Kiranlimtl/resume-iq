from embeddings import get_embedding
from resume_parser import resume_section_extractor
import numpy as np

def similarity_scores(job_desc):

    resume_embeddings = resume_section_extractor()
    job_desc_embedding = get_embedding(job_desc)
    similartiy_scores = []

    def consine_similarty(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    for section in resume_embeddings:
        similarity = consine_similarty(section["embedding"], job_desc_embedding[0].values)
        similartiy_scores.append({
            "section": section["section"],
            "similarity": similarity,
            "content": section["content"]
        })

    similartiy_scores.sort(key=lambda x: x["similarity"], reverse=True)
    content = [{section["section"]: section["content"]} for section in similartiy_scores]

    return content[:3], job_desc