from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os

app = FastAPI()
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store securely in Render

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
    1. Provide a professional detailed song feedback.
    2. Rate its commercial potential (1-100).
    3. Suggest 3-5 actionable rewrite tips.
    4. Suggest title alternatives.
    5. Offer co-writing enhancement ideas.
    6. Suggest production arrangement adjustments.
    7. Summarize overall label readiness.
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
