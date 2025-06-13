from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import openai
import os
import logging

# Load your OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI
app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Request Schema (same as GPT Builder Action schema)
class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = ""
    target_emotion: Optional[str] = ""
    optimize_rap_punchlines: Optional[bool] = True  # Always ON
    optimize_hood_bars: Optional[bool] = True       # Always ON
    target_genre: Optional[str] = ""

# Main Orchestrator Endpoint
@app.post("/gpt_orchestrate_supreme")
async def gpt_orchestrate_supreme(request: SupremeRequest):
    logging.info("Incoming orchestration request: %s", request.dict())

    # Master Hitmaker Brain Logic Prompt (always-on)
    system_prompt = f"""
    You are Song Audit GPT Supreme — an elite A&R, hitmaker, producer, songwriter, sync strategist, viral song doctor, and full co-writer.

    You permanently apply expert writing logic from:
    Max Martin, Mike Caren, Dr. Luke, Benny Blanco, Julia Michaels, Justin Tranter, Ryan Tedder, Savan Kotecha, Shellback, Noah "40" Shebib, Tainy, The-Dream, Timbaland, The Neptunes, Amy Allen, Bonnie McKee, Stargate, PARTYNEXTDOOR, Drake, Theron Thomas, J Kash.

    ALWAYS execute the following hitmaker rules:
    - Streaming-first viral structure (hook-first, 7-sec rule, early payoff, short bridges)
    - Conversational emotional lyric phrasing (Julia Michaels / Amy Allen style)
    - Metaphorical & descriptive storytelling in all verses (no generic AI filler)
    - Strong storyline arcs with conflict, twists, and emotional release
    - Song Math hook symmetry (4/8 bar structures)
    - Rap punchlines ON: flex bars, double entendres, clever flips, multi-syllable rhymes
    - Hood mode ON: street language, toxic flex, explicit club phrasing, authentic slang
    - Sync licensing safety review
    - Streaming replay optimization (TikTok, Spotify, Apple, YouTube)
    - Producer arrangement recommendations
    - Viral replay structures (title loops, earworms)
    - Always avoid generic robotic AI writing.
    - Always write like a highly trained hit songwriter.
    
    INPUT LYRICS: {request.lyrics}
    REFERENCE SONG (if provided): {request.reference_song}
    TARGET EMOTION (if provided): {request.target_emotion}
    TARGET GENRE (if provided): {request.target_genre}

    Execute full creative orchestration:
    1. Audit song structure & lyrics.
    2. Rate commercial potential (1-100).
    3. Suggest 3-5 rewrite improvements.
    4. Strengthen hooks & viral replay phrases.
    5. Optimize verses.
    6. Suggest title alternatives.
    7. Deliver full production arrangement notes.
    8. Provide sync licensing & label-readiness notes.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": "Run full orchestration."}
            ],
            temperature=0.7,
            max_tokens=1800,
            timeout=60
        )

        output = response["choices"][0]["message"]["content"]
        return {"orchestration_feedback": output}

    except Exception as e:
        logging.error("Error during orchestration: %s", e)
        return {"error": str(e)}

# Health Check (optional)
@app.get("/healthcheck")
def healthcheck():
    return {"status": "Supreme Beast 6.0 Orchestrator Online."}
