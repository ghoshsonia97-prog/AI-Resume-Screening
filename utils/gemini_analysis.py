import os
import json
from groq import Groq

def analyze_resume(resume_text: str, job_description: str) -> dict:
    """
    Analyzes a candidate's resume against a job description using Groq Cloud.
    Returns a structured dictionary compatible with the Streamlit app schema.
    """
    # 1. Initialize the Groq client using your environment variable
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        return {
            "summary": "Error: GROQ_API_KEY environment variable is missing on this machine.",
            "recommendation": "Potential",
            "matched_skills": [],
            "missing_skills": []
        }
        
    client = Groq(api_key=api_key)
    
    # 2. Force structural layout formatting within the system prompt context
    system_prompt = (
        "You are an expert Enterprise ATS Optimization Engine. Your task is to analyze "
        "the provided resume text against the target Job Description context. "
        "You must respond ONLY with a single valid JSON object. Do not include markdown code block formatting "
        "like ```json or any conversational prelude/postlude.\n\n"
        "The JSON object must contain exactly these 4 keys:\n"
        "1. \"summary\": A detailed professional engineering paragraph summarizing the candidate's core strengths.\n"
        "2. \"recommendation\": Exactly one of these choices: \"Strong Fit\", \"Good Fit\", or \"Potential\".\n"
        "3. \"matched_skills\": A list of strings representing specific skills matching the job description.\n"
        "4. \"missing_skills\": A list of strings representing specific gaps or missing skills relative to the job description."
    )
    
    user_content = f"--- TARGET JOB DESCRIPTION ---\n{job_description}\n\n--- CANDIDATE RESUME TEXT ---\n{resume_text}"
    
    try:
        # 3. Call the Groq Chat Completion API using the active production-supported Llama 3.3 70B
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            response_format={"type": "json_object"} # Enforces strict JSON output validation
        )
        
        # 4. Parse response safely
        raw_response = completion.choices[0].message.content
        parsed_analysis = json.loads(raw_response)
        return parsed_analysis

    except Exception as e:
        # Fallback dictionary prevents dashboard layout breaks if a runtime exception hits
        return {
            "summary": f"Automated structural extraction failed during pipeline compilation: {str(e)}",
            "recommendation": "Potential",
            "matched_skills": ["Data Processing"],
            "missing_skills": ["Pipeline Validation"]
        }