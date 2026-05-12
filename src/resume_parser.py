import json
import pdfplumber
from embeddings import get_embedding
import os
from collections import Counter

def get_resume_path():
    files = os.listdir("data")
    pdfs = [f for f in files if f.endswith(".pdf")]
    if not pdfs:
        raise FileNotFoundError("No resume found in data folder")
    return os.path.join("data", pdfs[0])

def resume_section_extractor():
    sections = {}
    embed_store = []

    if os.path.exists("data/embed_store.json"):
        with open("data/embed_store.json", "r") as f:
            embed_store = json.load(f)
        return embed_store
    else:
        resume_path = get_resume_path()

        with pdfplumber.open(resume_path) as pdf:
            for page in pdf.pages:
                words = page.extract_words(extra_attrs=["fontname", "size"])

                count_font = Counter([word["size"] for word in words])
                most_common_size = count_font.most_common(1)[0][0]
                second_most_common_size = count_font.most_common(2)[1][0]
                
                curr_sect_name = []
                curr_sect = []

                for word in words:
                    if word["size"] == second_most_common_size and curr_sect and curr_sect_name:
                        sections["".join(curr_sect_name)] = "".join(curr_sect)
                        curr_sect_name = [word["text"]]
                        curr_sect = []
                    elif word["size"] == second_most_common_size:
                        curr_sect_name.append(word["text"])
                    elif word["size"] == most_common_size and curr_sect_name:
                        curr_sect.append(" "+ word["text"])

        
            for section in sections:
                embeddings = get_embedding(sections[section])
                embed_store.append({
                    "section": section,
                    "embedding": embeddings[0].values,
                    "content": sections[section]
                })
            json.dump(embed_store, open("data/embed_store.json", "w"), indent=4)
    return embed_store
