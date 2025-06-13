from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import openai
import os
from dotenv import load_dotenv

# Load environment variables for OpenAI Key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# ==== SCHEMAS ====
class GPTOrchestrateRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = None
    target_emotion: Optional[str] = None
    optimize_rap_punchlines: Optional[bool] = False
    optimize_hood_bars: Optional[bool] = False
    target_genre: Optional[str] = None
    mode: Optional[str] = "rewrite"
    vibe_mode: Optional[str] = None
    era_mode: Optional[str] = None
    gender_pov: Optional[str] = None
    emotion_scaler: Optional[str] = None
    interpolation_request: Optional[str] = None

class QuickSongRequest(BaseModel):
    prompt: str

# ==== MASTER RULE STACK ====

HIT_RULES = """
General Hit Rules:
- Write fully natural, modern, highly conversational lyrics
- Use full human emotional subtext layering
- Advanced subtext, hidden meaning, ambiguity always present
- Avoid generic phrases, always write with unique metaphors and angles
- Strong opening bars/hooks mandatory (streaming-first intro)
- Explicit language allowed for Rap, R&B, Hip-Hop, Pop, when fitting
- Use sexual innuendo, metaphors, suggestive phrasing like human hit writers
- Use real cultural slang, regional lingo, generational (Millennial, Gen Z, Gen Alpha)
- Ebonics allowed naturally for rap and hip-hop writing where applicable
- Use fully human rap punchlines, clever wordplay, multi-syllable rhyme schemes
- Use fully human street-level hood bars (when activated)
- Conversational verses modeled after Julia Michaels / Amy Allen in Pop/R&B
- Always descriptive, "show don't tell", using senses (taste, touch, smell, etc.)
- Build emotional arcs, tension, payoff & storyline when applicable
- Avoid lazy filler writing at all times, no safe robotic AI word association
- Write using slang when it fits the lyric
- Use Similes like humans do
- Always try and be descriptive 
- Theme writing, so there is an over all theme to the song
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
- Always industry, sync, and label ready — no forced rhymes, no poetry vibes
- Keep plot motion moving forward per section, especially verses
- Dynamic rhyme flips, surprise lyrical twists, commercial wordplay
- Always inject clever, suggestive, provocative when genre calls for it
"""

EXTRA_WRITING_RULES = """
Advanced Writing & Structure Rules:
- Fully follow Max Martin, Stargate, Mike Caren, Jason Evigan, Ilya, Benny Blanco, Dr. Luke, PartyNextDoor, Amy Allen, Julia Michaels hit frameworks
- Fully dynamic streaming-first structure (hook-first, viral hook math, 7 second intro, short bridges)
- Build TikTok ready chantable phrases, anthemic call-and-response hooks
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
- Build full storyline for Country, Pop, and commercial crossover
- Interpolation Engine logic: honor flip requests while staying legally safe
- Song Flipping Engine: reverse perspective, gender swap POV if requested
- Vibe Mode: adapt writing style to requested artist vibe (SZA, Cardi B, PND etc.)
- Era Mode: adapt songwriting style to era (Y2K, 2010s, 2020s etc.)
- Gender POV engine for narrative perspective customization
- Emotion Scaler Engine (i.e.: "amp up heartbreak" or "make it nastier")
- Add sensory cinematic lyric details in all genres
- Build full label-room demo quality topline lyrics
"""

INFLUENCES = """
Influences Reference (Internal Modeling Only):
Max Martin, Dr. Luke, Benny Blanco, Stargate, The Neptunes, Timbaland, PartyNextDoor, Julia Michaels, Amy Allen, Bonnie McKee, J Kash, Theron Thomas, Drake, Jason Evigan, Ilya, Ed Sheeran, Mike Caren
"""

SUNO_FORMAT_GUIDE = """
Suno/Udio Prompt Formatting:
- Use [Section: ...] labels (ex: [Verse 1: emotional, sensual, conversational])
- Insert all Suno tags directly before target word: [vocal run] word, [adlibs], [harmonies], [stacked vocals], [backing vocals]
- No artist name or copyrighted melody references
- Follow Travis Nicholson + HowToPromptSuno advanced writing structures
- Reference: https://howtopromptsuno.com
- Reference: https://travisnicholson.medium.com/complete-list-of-prompts-styles-for-suno-ai-music-2024-33ecee85f180
"""

# ==== PROMPT BUILDER ====

def build_prompt(data: GPTOrchestrateRequest):
    prompt = f"""
You are a platinum-level hit songwriter, lyric optimizer, and professional A&R analyst.

TASK: Rewrite, optimize, and fully audit these provided lyrics for commercial hit-level performance.

{HIT_RULES}
{EXTRA_WRITING_RULES}
{INFLUENCES}
{SUNO_FORMAT_GUIDE}

Genre: {data.target_genre or 'General Pop/Rap/R&B'}
Target Emotion: {data.target_emotion or 'Radio-Ready Emotion Stack'}
Vibe Mode: {data.vibe_mode or 'Default'}
Era Mode: {data.era_mode or 'Current Top 40'}
Gender POV: {data.gender_pov or 'Default POV'}
Emotion Scaler: {data.emotion_scaler or 'Default Intensity'}
Interpolation Request: {data.interpolation_request or 'N/A'}
Optimize Rap Punchlines: {data.optimize_rap_punchlines}
Optimize Hood Bars: {data.optimize_hood_bars}
Reference Song: {data.reference_song or 'N/A'}

Rewrite and audit the provided lyrics into full commercial hit format. Apply full hitmaker logic stack.

---
{data.lyrics}
---

Return only fully structured final lyrics using Suno/Udio [Section: ] formatting.
NEVER provide explanation, notes, or comments — output pure final lyrics only.
"""
    return prompt

# ==== MAIN ORCHESTRATOR ENDPOINT ====
@app.post("/gpt_orchestrate_supreme")
def gpt_orchestrate_supreme(request: GPTOrchestrateRequest):
    prompt = build_prompt(request)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a platinum-level hit songwriter and advanced lyric optimizer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.88,
        max_tokens=3000
    )

    output = response.choices[0].message.content
    return {"result": output}

# ==== NATURAL LANGUAGE SONG GENERATOR ====
@app.post("/quick_song")
def quick_song(request: QuickSongRequest):
    user_prompt = f"""
You are a platinum-level hit songwriter generating a fully original song from natural language input.

{HIT_RULES}
{EXTRA_WRITING_RULES}
{INFLUENCES}
{SUNO_FORMAT_GUIDE}

User Request: 
{request.prompt}

Generate full commercial hit song using [Section: ] format with proper Suno/Udio tags, vocal runs, harmonies, adlibs, stacked vocals. Output only full lyrics — NO explanation.
"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a platinum-level hit songwriter."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.88,
        max_tokens=3000
    )

    output = response.choices[0].message.content
    return {"result": output}
