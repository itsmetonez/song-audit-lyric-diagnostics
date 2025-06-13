import openai
from fastapi import FastAPI
from pydantic import BaseModel

# Create FastAPI instance
app = FastAPI()

# Your OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Model for incoming request
class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: str = None
    target_emotion: str = None
    optimize_rap_punchlines: bool = False
    optimize_hood_bars: bool = False
    target_genre: str = None

# The master prompt
SUPREME_ORCHESTRATOR_PROMPT = """
You are Song Audit Supreme — a hit songwriting analysis and co-writing engine that merges:

Max Martin's melodic math, Stargate's simplicity, Benny Blanco's pop intuition, Timbaland's rhythmic punch, Neptunes' creative pockets, Drake's relatable vibe writing, Amy Allen & Julia Michaels emotional conversational lyricism, JKash & Theron Thomas pop-rap crossover mastery, PartyNextDoor's melodic trap phrasing, and Bonnie McKee's soaring top-lines.

Strictly avoid generic phrases. Focus on:
- Punchy openers
- Conversational, natural language
- Hooks that sound like real artists
- Vivid imagery
- Layered wordplay (especially rap)
- Metaphors and strong emotional resonance
- Current industry hit logic (playlist-friendly, TikTok punch, hit science)
- Apply "Song Math" rules: correct symmetry, repetition, tension/release, and dynamic energy.
- Blend reference artist/song DNA naturally into the writing without copying exact phrases.
- You can curse or include explicit language where authentic to genre.
- Allow cultural nuance for rap, R&B, country or trap where relevant.

Song draft for full audit and optimization:
"""

@app.post("/gpt_orchestrate_supreme")
async def gpt_orchestrate_supreme(request: SupremeRequest):
    try:
        custom_instructions = SUPREME_ORCHESTRATOR_PROMPT
        custom_instructions += f"\nOriginal lyrics:\n{request.lyrics}\n"
        if request.reference_song:
            custom_instructions += f"Reference Song: {request.reference_song}\n"
        if request.target_emotion:
            custom_instructions += f"Target Emotion: {request.target_emotion}\n"
        if request.target_genre:
            custom_instructions += f"Target Genre: {request.target_genre}\n"
        if request.optimize_rap_punchlines:
            custom_instructions += "Apply strong punchline layering for rap format.\n"
        if request.optimize_hood_bars:
            custom_instructions += "Allow authentic street/hood energy and phrasing.\n"

        # GPT call
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": custom_instructions},
                {"role": "user", "content": "Run full Supreme optimization and A&R hit audit."}
            ],
            temperature=0.7,
            max_tokens=1500,
            timeout=30
        )

        full_output = response.choices[0].message.content
        return {"result": full_output}

    except Exception as e:
        return {"error": str(e)}
