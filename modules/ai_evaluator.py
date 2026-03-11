import os
import json
from google import genai
from google.genai import types

def evaluate_candidate(resume_text, job_description):
    """
    Sends prompt to Google Gemini API and parses the JSON response.
    """
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key or api_key == 'your_key_here':
        raise ValueError("Valid GEMINI_API_KEY environment variable is required.")
        
    client = genai.Client(api_key=api_key)
    
    prompt = f"""
    Analyze this resume against the job description.
    Return ONLY a valid JSON object with these exact keys:
    candidate_name, match_score (integer 0-100), strengths (string),
    missing_skills (string), recommendation (exactly one of: "Strong Fit",
    "Moderate Fit", "Not a Fit"), risk_assessment (exactly one of:
    "Low Risk", "Moderate Risk", "High Risk"), candidate_summary (string).
    
    JOB DESCRIPTION:
    {job_description}
    
    RESUME:
    {resume_text}
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
            ),
        )
        # Parse the JSON response
        result_text = response.text
        # Clean up any potential markdown formatting the model might still add
        if result_text.startswith("```json"):
            result_text = result_text[7:-3].strip()
        elif result_text.startswith("```"):
            result_text = result_text[3:-3].strip()
            
        evaluation_result = json.loads(result_text)
        return evaluation_result
    except Exception as e:
        print(f"Error during AI evaluation: {e}")
        return None
