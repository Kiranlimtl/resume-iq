from embeddings import get_embedding
from resume_parser import resume_section_extractor
import numpy as np

def similarity_scores():

    job_desc = """ About the job

        Job Requisition ID #

        25WD94021

        Position Overview

        The IAM (Identity and Access Management) group at Autodesk is seeking a passionate Intern Software Engineer with skills in Java or GoLang to join our dynamic team. This is a unique opportunity to work on cutting-edge technology and contribute to the development of secure and scalable identity solutions.

        What We Offer

            Hands-on experience with industry-leading software and technologies
            Mentorship from experienced professionals in the field.
            A collaborative and inclusive working environment.
            Opportunities to engage with various teams and projects within Autodesk
            Potential for future career opportunities within the company

        Responsibilities

            Assist in the design, development, and maintenance of software applications using Java or GoLang
            Collaborate with senior engineers and participate in code reviews
            Write clean, scalable, and efficient code under the guidance of your mentor
            Debug and troubleshoot issues in the development environment
            Participate in daily stand-ups and contribute to team discussions
            Document code and participate in the creation of technical documentation

        Minimum Qualifications

            Currently enrolled in a Bachelor's degree program in Computer Science, Computer Engineering, or a related field, graduating in 2026 or 2027
            Strong understanding of object-oriented programming and design principles
            Proficiency in Java or GoLang; familiarity with both is a plus
            Basic knowledge of software development methodologies like Agile/Scrum
            Internship duration: June - December 2026, 6 months full-time only

        Preferred Qualifications

            Experience with version control systems such as Git
            Familiarity with RESTful APIs and microservices architecture
            Understanding of database technologies and SQL
            Exposure to cloud platforms like AWS, Azure, or Google Cloud
            Knowledge of identity and access management concepts is a plus

        About Autodesk 

        With Autodesk software, you have the power to Make Anything. The future of making is here, bringing with it radical changes in the way things are designed, made, and used. It is disrupting every industry: architecture, engineering, construction, manufacturing, and media and entertainment. With the right knowledge and tools, this disruption is your opportunity.

        Learn More

        About Autodesk

        Welcome to Autodesk! Amazing things are created every day with our software – from the greenest buildings and cleanest cars to the smartest factories and biggest hit movies. We help innovators turn their ideas into reality, transforming not only how things are made, but what can be made.

        We take great pride in our culture here at Autodesk – it’s at the core of everything we do. Our culture guides the way we work and treat each other, informs how we connect with customers and partners, and defines how we show up in the world.

        When you’re an Autodesker, you can do meaningful work that helps build a better world designed and made for all. Ready to shape the world and your future? Join us!

        Salary transparency

        Salary is one part of Autodesk’s competitive compensation package. Offers are based on the candidate’s experience, educational level, and geographic location.

        Diversity & Belonging

        We take pride in cultivating a culture of belonging where everyone can thrive. Learn more here: https://www.autodesk.com/company/diversity-and-belonging"""

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