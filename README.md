# Resume IQ

A Streamlit web app that uses Gemini as an AI agent to analyze a resume against a job description and provide improvement feedback.

## Architecture

The project has three layers: a Streamlit frontend, an agentic tool-use loop, and a set of tools backed by embeddings and LLM calls.

### Frontend — `src/app.py`

- User pastes a job description and uploads a PDF resume
- Both are saved to a `data/` folder
- Clicking "Analyze Resume" calls `run_agent()` and renders the markdown result

### Agent Loop — `src/agent.py`

A manual agentic tool-use loop using the Gemini API (`google-genai` SDK). Four tools are registered as function declarations with a system prompt that instructs Gemini to always start with `search_resume`.

The `while True` loop sends the conversation to Gemini and checks each response:
- **Function call** — routes to the matching Python function, appends the tool result back into the conversation, and loops again
- **Text response** — the agent is done, returns the final answer to the UI

This is a ReAct-style agent where Gemini decides which tools to call and in what order. No framework (LangChain, etc.) is used — the loop is built from scratch.

### Tools — `src/tools/`

| Tool | What it does |
|---|---|
| `search_resume` | Entry point tool. Uses embeddings + cosine similarity to find the top 3 most relevant resume sections for the job description. |
| `get_missing_keywords` | Calls Gemini to list keywords/skills in the job description that are missing from the resume. |
| `resume_analysis` | Calls Gemini for a full analysis: match score, missing keywords, rewrite suggestions, and action plan. |
| `rewrite_bullet_pts` | Calls Gemini to rewrite resume bullet points to be more impactful and tailored to the job description. |

## Embedding and Search Pipeline

This is the RAG-like component that powers `search_resume`.

1. **`resume_parser.py`** — Parses the PDF using `pdfplumber` and extracts words with font metadata (name, size). Uses font size frequency to split the resume into sections: the second-most-common font size is treated as section headers, and the most-common size as body text. This avoids hardcoded header names.

2. **`embeddings.py`** — Calls `gemini-embedding-2` to embed each section's text.

3. **`similarity.py`** — Embeds the job description, computes cosine similarity between the job description embedding and each resume section embedding, and returns the top 3 most relevant sections.

4. Results are cached in `data/embed_store.json` keyed by filename, so re-runs don't re-embed the same resume.

## Flow

```
User clicks "Analyze Resume"
  -> run_agent("Analyze my resume for: <job desc>")
    -> Gemini calls search_resume(job_desc)
      -> PDF parsed -> sections embedded -> cosine similarity -> top 3 sections returned
    -> Gemini calls resume_analysis / get_missing_keywords / rewrite_bullet_pts
      -> each makes its own Gemini call with the relevant sections + job description
    -> Gemini composes a final text response
  -> rendered as markdown in Streamlit
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_key_here
   ```

3. Run the app:
   ```
   streamlit run src/app.py
   ```

## Tech Stack

- **LLM**: Gemini 2.5 Flash Lite (agent + tool calls), Gemini Embedding 2 (embeddings)
- **Frontend**: Streamlit
- **PDF Parsing**: pdfplumber
- **Similarity**: NumPy (cosine similarity)
