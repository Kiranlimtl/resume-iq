from google.genai import types
from google import genai
import os
from tools.miss_keywords import get_missing_keywords_declaration, get_missing_keywords
from tools.resume_analyse import resume_analysis_declaration, resume_analysis
from tools.rewrite_bullet_pts import rewrite_bullet_pts_declaration, rewrite_bullet_pts
from tools.search_resume import search_resume, search_resume_declaration, search_resume

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
tools = types.Tool(function_declarations=[
    get_missing_keywords_declaration,
    rewrite_bullet_pts_declaration,
    resume_analysis_declaration,
    search_resume_declaration
])
config = types.GenerateContentConfig(
    tools=[tools],
    system_instruction="""You are a resume improvement agent. 
        You MUST use the available tools to help the user. 
        Always start by calling search_resume with the job description 
        to find relevant sections before doing anything else."""
)


def run_agent(user_message, contents=[]):
    contents.append(types.Content(
        role="user",
        parts=[types.Part.from_text(text=user_message)]
    ))
    while True:
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=contents,
                config=config,
            )
        except Exception as e:
            if "429" in str(e):
                return "Rate limited — please wait a minute and try again."
            return f"Error: {e}"

        if not response.candidates or not response.candidates[0].content.parts:
            return "Sorry, I got an empty response. Try again."
        
        part = response.candidates[0].content.parts[0]
        
        # if no tool call, gemini is done — print final answer
        if not part.function_call:
            print(response.text)
            return response.text
        
        tool_call = part.function_call
        print(f"Calling tool: {tool_call.name}")
        
        # route to the right function
        if tool_call.name == "search_resume":
            result = search_resume(tool_call.args["job_desc"])
        elif tool_call.name == "get_missing_keywords":
            result = get_missing_keywords(tool_call.args["content"], tool_call.args["job_desc"])
        elif tool_call.name == "resume_analysis":
            result = resume_analysis(tool_call.args["content"], tool_call.args["job_desc"])
        elif tool_call.name == "rewrite_bullet_pts":
            result = rewrite_bullet_pts(tool_call.args["content"], tool_call.args["job_desc"])
        
        # append model response and tool result back to conversation
        contents.append(response.candidates[0].content)
        contents.append(types.Content(
            role="user",
            parts=[types.Part.from_function_response(
                name=tool_call.name,
                response={"result": str(result)},
            )]
        ))