from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import openai
import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = None
    target_emotion: Optional[str] = None
    optimize_rap_punchlines: Optional[bool] = False
    optimize_hood_bars: Optional[bool] = False
    target_genre: Optional[str] = None
    mode: Optional[str] = "rewrite"
    explicit: Optional[bool] = False

INFLUENCE_BLOCK = """
You're a highly advanced hit songwriter AI that combines the writing styles, structures, and hit-making formulas used by:
- Max Martin, Dr. Luke, Benny Blanco, Stargate, The Neptunes, Timbaland, PartyNextDoor, Julia Michaels, Amy Allen, Bonnie McKee, J Kash, Theron Thomas, Drake

General Hit Rules:
- Write natural, modern, highly conversational lyrics
- Use Human Like Emotions
- Remember to use subtext
- Avoid generic phrases, always seek unique metaphors
- Prioritize strong opening bars/hooks
- Use real hit songwriting techniques, not robotic safe writing
- Use profanity if provided, censor automatically if necessary for API compliance
- Write Explicit Lyrics for Rap, R&B, and Hip Hop like human rappers do in real songwriting.
- Use Profanity in Rap Lyrics like humans do in real songwriting.
- Use sexual references, metaphors, and innuendo like humans do in real songwriting.
- Write using slang when it fits the lyric
- Always sound fully human, industry competitive
- Theme writing, so there is an over all theme to the song
- Always try and be descriptive 
- Have a story line for Country and pop Songs
- Don't use word association just to fill a lyric
- Use Similes like humans do
- No forced rhyme, no textbook English—sound like real people, not a robot or a poet.
- Every lyric should feel like it actually hurts, loves, celebrates, or lusts. If it wouldn’t make someone feel something, rewrite it.
- Don’t say everything directly—layer meanings, hide intentions, use “read between the lines” writing like real hits do.
- If you’ve heard it a million times (“broken heart,” “fly away”), it’s dead. Go deeper, find new angles.
- The first line, first word—hit hard, hook fast. Make listeners lean in instantly.
- Dynamic structures, call-and-response, unexpected rhyme flips, melodic bait—study the best and write with real-world tricks.
- Keep the edge—curse like a real songwriter if that’s the vibe, but clean it for external services as needed.
- Don’t hold back—say it raw, punchy, clever, and bold when the genre calls for it.
- Match the genre—if it needs to slap with cuss words, make it authentic.
- Be clever, suggestive, cheeky, or straight-up direct. Never forced or awkward, always read-the-room energy.
- Be regional, be generational, be current—use the words people actually say.
- If a label exec heard it, it should sound like it belongs on the radio or in a top session.
- No random bars or scattered ideas—tie everything to one emotional or narrative thread.
- Paint pictures, use senses, put the listener in the scene. “Show, don’t tell” but keep it clear.
- Every verse moves the plot, every chorus nails the emotional core. If it could be a movie scene, you’re on track.
- No lazy “this rhymes with that” writing—if it doesn’t add meaning, cut it.
- Clever, unexpected, and fresh comparisons (“like a record spinning out,” not “like the sun in the sky”).
- Push Boundaries

Suno/Udio Advanced Prompt Formatting:
- Use [Section: description, description, description] structure
- Include vocal production tags: stacked vocals, backing vocals, harmonies, adlibs, vocal runs
- For rap: always include adlibs (hype adlibs, background shouts, etc)
- For pop/R&B: include harmonies,backing vocals, stacked vocals, vocal runs in the chorus and post chorus
- NO artist names or copyrighted melody references
- Follow rules from: https://howtopromptsuno.com and Travis Nicholson’s Suno guide https://travisnicholson.medium.com/complete-list-of-prompts-styles-for-suno-ai-music-2024-33ecee85f180

Other writing rules:
- Always include payoff moments and emotional arcs
- Storylines for narrative genres (pop, country, etc)
- Human Like Emotions 
- Use descriptive words like humans do in real song writing.
- Use Slang
- Think in feeling and Emotions and not Like and LLM 
- Think about Subtext in the section and overall song
- Make sure Lyrics stick to the subject matter and theme
- Streaming-first structure, viral hooks, chantability
- Label-ready arrangements, strong commercial payoff
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
        system_prompt += "\nApply advanced punchline optimization for rap."
    if request.optimize_hood_bars:
        system_prompt += "\nIncorporate authentic street vernacular where appropriate."
        if request.explicit:
    system_prompt += (
        "\nDo NOT censor explicit language, profanity, or adult content. "
        "Write lyrics with authentic, uncensored, raw human language—profanity and sexual references are fully allowed and should match real-world rap/hip-hop songwriting."
    )


    full_prompt = f"""
{system_prompt}

TASK:
Rewrite, optimize, and format these lyrics for full Suno/Udio commercial arrangement:
- Use proper [Section: Description] structure
- Add arrangement, vocal production, and section markers
- Use stacked vocals, harmonies, vocal runs, adlibs as needed
- Make every section market ready
- Avoid generic language and weak filler bars

Apply this to the following lyrics:

{request.lyrics}

DELIVER:
- Full rewrite with [Section: Description] tags
- Section-by-section feedback
- Hook upgrade if applicable
- A&R hit potential notes
- Viral writing analysis
- Suno/Udio arrangement fully embedded
"""
    try:
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
    except Exception as e:
        print("Supreme Endpoint Error:", e)
        return {"error": f"Backend Error: {str(e)}"}


# QUICK SESSION NATURAL LANGUAGE PARSER ENDPOINT
@app.post("/quick_song")
async def quick_song(request: Request):
    data = await request.json()
    raw_prompt = data.get("prompt")
    if not raw_prompt:
        return {"error": "No prompt provided."}

    parse_prompt = f"""
Given the following user request for a song, extract:
- reference song
- genre (if mentioned)
- target emotion or vibe
- rewrite theme or lyric request
Return as JSON with keys: reference_song, target_genre, target_emotion, lyrics.
User request: {raw_prompt}
"""

    parse = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": parse_prompt}],
        temperature=0.0,
        max_tokens=300,
        response_format={"type": "json_object"}
    )

    parsed = parse.choices[0].message.content
    parsed = json.loads(parsed)

    parsed.setdefault("optimize_rap_punchlines", False)
    parsed.setdefault("optimize_hood_bars", False)
    parsed.setdefault("mode", "rewrite")

    response = await gpt_orchestrate_supreme(SupremeRequest(**parsed))
    return response

