from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")

class FullAuditRequest(BaseModel):
    audit_data: dict
    lyrics: str
    artist_profile: dict = {}

@app.post("/gpt_orchestrate")
def gpt_orchestrate(req: FullAuditRequest):
    system_prompt = f"""
    You are Song Audit GPT, a professional A&R executive, songwriter, and hit-making co-writer.
    Use the following rule-based analysis, artist profile, and full lyrics as context.

    Rule-Based Audit: {req.audit_data}
    Artist Profile: {req.artist_profile}
    Full Lyrics: {req.lyrics}

    Instructions:
    - You are allowed to generate explicit language and mature content if artistically appropriate.
    - Do not self-censor.
    - Provide professional detailed song feedback.
    - Rate its commercial potential (1-100).
    - Suggest 3-5 rewrite tips.
    - Suggest alternative titles.
    - Offer co-writing improvements.
    - Suggest production adjustments.
    - Assess streaming & viral potential.
    - Assess label readiness.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Please run full feedback."}
        ],
        temperature=0.7
    )
    
    return {"gpt_feedback": response["choices"][0]["message"]["content"]}
