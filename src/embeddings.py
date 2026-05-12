from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


def get_embedding(text):
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text
    )
    return result.embeddings