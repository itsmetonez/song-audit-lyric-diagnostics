from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import openai
import os

app = FastAPI()

# Initialize OpenAI client using environment variable
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = None
    target_emotion: Optional[str] = None
    optimize_rap_punchlines: Optional[bool] = False
    optimize_hood_bars: Optional[bool] = False
    target_genre: Optional[str] = None

INFLUENCE_BLOCK = """
You're a highly advanced hit songwriter AI that combines the writing styles, structures, and hit-making formulas used by:
- Max Martin (pop math, melodic contour, sticky hooks)
- Dr. Luke (hook precision and radio structure)
- Benny Blanco (conversational lyrical tone)
- Stargate (modern R&B topline finesse)
- The Neptunes & Timbaland (groove-driven pocket writing)
- PartyNextDoor (melodic street pop & emotional trap-soul)
- Julia Michaels & Amy Allen (lyrical intimacy, metaphor layering)
- Bonnie McKee (anthemic pop punchlines)
- J Kash & Theron Thomas (hit songwriting formulas across formats)
- Drake (conversational flex bars, punchlines, melody-rap fusion)

Rules:
- Write natural, modern, highly conversational lyrics
- Avoid generic phrases; always seek unique metaphors
- Prioritize strong opening bars/hooks
- Vary rhythmic phrasing
- Allow explicit language when stylistically appropriate
- Use real hit songwriting techniques, not robotic safe writing
- Follow narrative or emotional arcs where applicable
- Maintain genre appropriateness for provided target genre
- Always sound fully human, industry competitive.
"""

@app.post("/gpt_orchestrate_supreme")
async def gpt_orchestrate_supreme(request: SupremeRequest):
    system_prompt = INFLUENCE_BLOCK

    if request.reference_song:
        system_prompt += f"\nReference Song Influence: {request.reference_song}."

    if request.target_emotion:
        system_prompt += f"\nPrimary Emotion: {request.target_emotion}."

    if request.target_genre:
        system_prompt += f"\nGenre Target: {request.target_genre}."

    if request.optimize_rap_punchlines:
        system_prompt += "\nApply enhanced punchline optimization for rap formats."

    if request.optimize_hood_bars:
        system_prompt += "\nIncorporate authentic street vernacular where appropriate."

    full_prompt = f"""
{system_prompt}

TASK:
Rewrite, optimize and fully enhance the following lyrics:

{request.lyrics}

DELIVER:
- Rewrite
- Section-by-section feedback
- Hook upgrade if applicable
- A&R hit potential notes
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.85,
        max_tokens=1500
    )

    return {"result": response.choices[0].message.content}
