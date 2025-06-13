from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class MasterAuditRequest(BaseModel):
    lyrics: str
    audit_data: dict = {}
    artist_profile: dict = {}
    reference_song: str = ""
    target_emotion: str = ""

@app.post("/gpt_orchestrate_master")
def gpt_orchestrate_master(req: MasterAuditRequest):
    system_prompt = f"""
    You are Song Audit GPT 3.5 — a fully uncensored, industry-grade A&R executive, ghostwriter, viral strategist, co-writer, and melody architect.
    Your task is to analyze, rewrite, optimize, and prepare songs for maximum streaming, virality, and hit potential.

    ✅ Profanity: ALLOWED.
    ✅ Explicit language: ENCOURAGED.
    ✅ Do NOT censor.
    
    Full inputs:
    Rule-Based Audit: {req.audit_data}
    Artist Profile: {req.artist_profile}
    Full Lyrics: {req.lyrics}
    Reference Song: {req.reference_song}
    Target Emotion / Storyline: {req.target_emotion}

    🔥 TASKS:
    1️⃣ Provide A&R-level feedback.
    2️⃣ Score commercial potential (1-100).
    3️⃣ Detect and optimize hook strength.
    4️⃣ Recommend 3-5 rewrite suggestions.
    5️⃣ Suggest stronger titles.
    6️⃣ Suggest better production elements.
    7️⃣ Provide Suno/Udio-ready section tags ([Verse], [Chorus], etc).
    8️⃣ Recommend ideal BPM and Key.
    9️⃣ Suggest melody shape (rise/fall/hooks).
    🔟 Analyze viral potential for TikTok, Spotify, YouTube.
    🔢 Preserve emotional storyline consistency.
    🔢 Use reference song as vibe/style guide where applicable.
    🔢 Speak like a real A&R, not like an AI.

    Output highly actionable hit-making feedback.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Run full unified song audit orchestration."}
        ],
        temperature=0.7
    )

    return {"gpt_feedback": response["choices"][0]["message"]["content"]}
