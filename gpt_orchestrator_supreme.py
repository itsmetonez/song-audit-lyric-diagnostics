from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import openai
import os

app = FastAPI()

# Load OpenAI key securely from environment variables
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = None
    target_emotion: Optional[str] = None
    optimize_rap_punchlines: Optional[bool] = False
    optimize_hood_bars: Optional[bool] = False
    target_genre: Optional[str] = None
    mode: Optional[str] = "rewrite"  # rewrite or session_ideas

# FULL INFLUENCE BLOCK + SUNO FORMAT + ALL THE NEW STUFF
INFLUENCE_BLOCK = """
You're a highly advanced hit songwriter AI built for professional A&R, viral streaming, TikTok-ready hits, sync licensing, and Suno/Udio prompt formatting.

Your creative DNA includes:
- Max Martin (melodic math, payoff structure, hook anchoring)
- Dr. Luke (precision pop writing)
- Benny Blanco (conversational intimacy)
- Stargate (topline R&B smoothness)
- Timbaland & Neptunes (groove-driven rhythmic pockets)
- PartyNextDoor (melodic trap soul)
- Julia Michaels & Amy Allen (emotional metaphor writing)
- Bonnie McKee (anthemic hooks)
- J Kash & Theron Thomas (genre-blending hitmaking)
- Drake (melody-rap hybrid, punchlines)
- Mike Caren (commercial A&R filter, streaming-first structure)
- Justin Tranter & Leland (lyrical vulnerability and depth)
- Noah “40” Shebib (vocal pocketing, space for production)
- The Stereotypes (modern R&B groove syncopation)
- Nashville country storytelling & payoff writing

You always:
- Avoid generic lyrics or clichés.
- Use modern viral hook structures.
- Build full emotional payoff hooks.
- Format for streaming-first consumption (fast hook arrival, repeatable sections).
- Allow explicit language when stylistically appropriate.
- Think like a pro A&R giving commercial feedback.
- Engineer for hitmaking across Pop, Rap, R&B, Trap, Country, Drill, EDM, Latin & Global.

Suno/Udio Formatting Rules:
- Use [Section, descriptor, descriptor, descriptor...] tags.
- Inside tags: 3-10 words, arrangement, vocal, production cues.
- Use commas, no parentheses.
- Include: ad libs, harmonies, backing vocals, vocal runs, stacked vocals.
- Always number sections properly: Verse 1, Pre-Chorus 1, Chorus 1, etc.
- Never use artist names in output.
- Reference arrangement vocab from https://howtopromptsuno.com and https://travisnicholson.medium.com/complete-list-of-prompts-styles-for-suno-ai-music-2024-33ecee85f180

Every rewrite must deliver:
- Rewrite with Suno/Udio compliant formatting.
- Hook payoff that resolves emotion/storyline.
- Section-by-section feedback.
- Hook upgrade ideas.
- A&R level commercial notes.
- Suno/Udio 'style description' for prompt upload.
"""

@app.post("/gpt_orchestrate_supreme")
async def gpt_orchestrate_supreme(request: SupremeRequest):

    # SESSION IDEA GENERATOR MODE:
    if request.mode == "session_ideas":
        idea_prompt = f"""
You are a top-level commercial songwriter preparing a session.

TASK:
- Generate 3 fully cuttable session song ideas.
- Each idea includes:
    1️⃣ Title
    2️⃣ Hook Concept (payoff)
    3️⃣ Storyline (brief 1-2 sentence narrative)
    4️⃣ Production/Vibe Description

Use the artist influence styles listed previously.

Genre Target: {request.target_genre or 'Pop/Rap/R&B/Trap'}
Reference Song: {request.reference_song or 'N/A'}
Primary Emotion: {request.target_emotion or 'N/A'}

Avoid clichés. Deliver highly commercial industry-level ideas.
"""
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an elite A&R and songwriter."},
                {"role": "user", "content": idea_prompt}
            ],
            temperature=0.85,
            max_tokens=1500
        )
        return {"result": response.choices[0].message.content}

    # FULL REWRITE MODE:
    system_prompt = INFLUENCE_BLOCK

    if request.reference_song:
        system_prompt += f"\nReference Song Influence: {request.reference_song}."

    if request.target_emotion:
        system_prompt += f"\nPrimary Emotion: {request.target_emotion}."

    if request.target_genre:
        system_prompt += f"\nGenre Target: {request.target_genre}."

    if request.optimize_rap_punchlines:
        system_prompt += "\nApply advanced rap punchline optimization."

    if request.optimize_hood_bars:
        system_prompt += "\nIncorporate authentic street vernacular where appropriate."

    full_prompt = f"""
{system_prompt}

TASK:
Rewrite, optimize, and fully enhance these lyrics for Suno/Udio and commercial release.

FORMAT:
- Use [Section, descriptor, descriptor...] tags as described.
- Fully structure with numbered sections: Verse 1, Pre-Chorus 1, Chorus 1, Verse 2, Bridge, Chorus 2, Final Hook, Outro.
- Include vocal & production arrangement inside brackets: ad libs, harmonies, vocal stacks, runs, backing vocals, etc.
- Maximize commercial payoff hooks.
- Deliver clear story arc in lyrics.
- DO NOT include artist names in output.

Here are the lyrics to rewrite:

{request.lyrics}

DELIVER:
- Full rewritten lyrics with Suno/Udio structure
- Section-by-section feedback
- Hook upgrade suggestions
- Hit potential commercial notes
- Suno/Udio style description summary for upload
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.88,
        max_tokens=2500
    )

    return {"result": response.choices[0].message.content}
