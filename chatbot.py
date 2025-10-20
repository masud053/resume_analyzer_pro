import os, openai
from typing import Optional

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def get_openai_feedback(resume_text: str, job_text: str, max_tokens: int = 600) -> str:
    if not OPENAI_API_KEY:
        return "OpenAI API key not set. Set OPENAI_API_KEY to enable GPT feedback."
    prompt = f"""You are an expert technical recruiter. Given the resume and the job description, provide:
1) Top 5 strengths (short)
2) Top 5 weaknesses / gaps (short)
3) Concrete bullet suggestions to improve the resume to match the job description
4) A short résumé summary that can be used as a LinkedIn headline.
Resume:
{resume_text}

Job description:
{job_text}
"""
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role':'user','content':prompt}],
        max_tokens=max_tokens,
        temperature=0.2
    )
    return resp['choices'][0]['message']['content']
