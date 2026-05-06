import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def evaluate_resume_with_llm(resume_text: str, job_description: str) -> dict:
    model_name = os.getenv("OPENAI_MODEL", "gpt-5.5")

    prompt = f"""
You are an HR screening assistant for entry-level hiring.

Your task:
Compare the candidate resume against the job description and produce a structured screening report.

Important rules:
- Do not make a final hiring decision.
- Do not use protected characteristics such as age, gender, race, nationality, religion, disability, or marital status.
- Base your evaluation only on job-relevant evidence from the resume and job description.
- If evidence is missing, say it is missing instead of assuming.
- Be fair, cautious, and specific.
- This tool is advisory only; a human recruiter must review the result.

Scoring rubric:
1. Relevant skills match: 0-30
2. Relevant experience/projects: 0-25
3. Education or training alignment: 0-15
4. Communication/leadership/teamwork evidence: 0-15
5. Overall job-readiness for entry-level role: 0-15

Return only valid JSON with this exact structure:
{{
  "match_score": 0,
  "candidate_level": "Strong Match / Moderate Match / Weak Match",
  "key_strengths": ["strength 1", "strength 2", "strength 3"],
  "key_weaknesses": ["weakness 1", "weakness 2"],
  "missing_skills": ["skill 1", "skill 2"],
  "risk_factors": ["risk 1", "risk 2"],
  "recommendation": "Shortlist / Maybe / Reject",
  "reasoning_summary": "short paragraph explaining the recommendation",
  "human_review_note": "short note explaining what a human recruiter should verify"
}}

Job Description:
\"\"\"
{job_description}
\"\"\"

Candidate Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    response = client.responses.create(
        model=model_name,
        input=prompt
    )

    output_text = response.output_text.strip()

    try:
        return json.loads(output_text)
    except json.JSONDecodeError:
        return {
            "match_score": None,
            "candidate_level": "Parsing Error",
            "key_strengths": [],
            "key_weaknesses": [],
            "missing_skills": [],
            "risk_factors": [],
            "recommendation": "Human Review Required",
            "reasoning_summary": output_text,
            "human_review_note": "The model did not return valid JSON. A human should review the raw output."
        }