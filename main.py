from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import openai
import os
import re

app = FastAPI()

# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")

########################################
# ✅ RULE-BASED ANALYSIS ENGINE (legacy audit)
########################################

cliche_list = [
    "chasing shadows", "heart on fire", "lost control", "broken pieces",
    "demons inside", "rise from the ashes", "falling for you", "fading away",
    "my broken heart", "tears falling down", "lost without you", "burning desire",
    "haunted by you", "main character energy", "stay toxic", "ghosted",
    "trust issues", "situationship", "low key", "high key", "matching energy",
    "trauma dump"
]

filler_words = [
    "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna",
    "i think", "gotta", "you know", "honestly", "truthfully", "literally",
    "basically", "obviously", "lowkey", "highkey", "somehow", "i swear",
    "actually", "forever", "never ever", "always", "right now", "even",
    "tryna", "somebody", "anyone", "no one"
]

predictable_rhymes = [
    ("you", "do", "too", "through", "true"),
    ("love", "above", "glove", "of"),
    ("heart", "apart", "start", "part"),
    ("pain", "rain", "again", "insane"),
    ("fire", "desire", "higher", "entire"),
    ("cry", "die", "lie", "why"),
    ("see", "me", "be", "free")
]

@app.post("/analyze")
def analyze_lyrics(request: dict):
    lyrics = request['lyrics'].lower()
    cliches = [phrase for phrase in cliche_list if phrase in lyrics]
    words = lyrics.replace("\n", " ").split()
    word_counts = Counter(words)
    repetition = [f"'{word}': {count} times" for word, count in word_counts.items() if count > 3]
    predictability_flags = []
    for rhyme_group in predictable_rhymes:
        count = sum(lyrics.count(word) for word in rhyme_group)
        if count >= 3:
            predictability_flags.append(f"Common rhyme group overused: {rhyme_group}")
    tighten_suggestions = [word for word in filler_words if word in lyrics]
    overall_notes = "Review flagged clichés, repetition, filler words, and predictable rhyme traps to sharpen originality."
    return {
        "cliches": cliches,
        "repetition": repetition,
        "predictability_flags": predictability_flags,
        "tighten_suggestions": tighten_suggestions,
        "overall_notes": overall_notes
    }

########################################
# ✅ SUPREME HITMAKER BRAIN ORCHESTRATOR 6.0
########################################

class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: str = ""
    target_emotion: str = ""
    optimize_rap_punchlines: bool = False
    optimize_hood_bars: bool = False
    target_genre: str = ""

@app.post("/gpt_orchestrate_supreme")
def gpt_orchestrate_supreme(req: SupremeRequest):
    system_prompt = f"""
    You are Song Audit GPT Supreme — an elite A&R, songwriter, producer, sync strategist, and commercial hitmaker.

    You permanently apply hitmaker writing logic from:
    Max Martin, Mike Caren, Dr. Luke, Benny Blanco, Julia Michaels, Justin Tranter, Ryan Tedder, Savan Kotecha, Shellback, Noah "40" Shebib, Tainy, The-Dream, Timbaland, The Neptunes, Amy Allen, Bonnie McKee, Stargate, PARTYNEXTDOOR, Drake, Theron Thomas, J Kash.

    Default rules always active:
    - Streaming-first viral structure (hook-first, 7-sec rule, fast payoff intro, short bridges).
    - Conversational lyric phrasing (Julia Michaels / Amy Allen / PND style).
    - Lyrical metaphor encouragement especially in emotional songs.
    - Descriptive detail-heavy verses — avoid generic filler AI writing.
    - Storyline arcs with conflict, emotional payoff, lyric twists.
    - Genre-adaptive phrasing based on {req.target_genre}.
    - Hook math symmetry (Max Martin 4/8 bar rule).
    - Rap punchlines (if enabled): flex bars, multi-syllable rhyme, clever flips.
    - Hood bars (if enabled): club energy, explicit, trap street language.
    - Sync licensing safety while keeping commercial edge.
    - Label readiness analysis for radio, streaming, TikTok, sync.
    - Suggest BPM, key, and possible Suno/Udio section tags.

    INPUT LYRICS: {req.lyrics}
    REFERENCE SONG: {req.reference_song}
    TARGET EMOTION: {req.target_emotion}
    RAP PUNCHLINE ENGINE: {req.optimize_rap_punchlines}
    HOOD MODE: {req.optimize_hood_bars}

    TASK:
    Run full professional creative orchestration:
    - Analyze commercial potential 1-100.
    - Suggest rewrite improvements.
    - Strengthen hook phrasing.
    - Improve verse structure.
    - Optimize viral structure.
    - Provide full co-writer level critique.
    - Suggest producer arrangement upgrades.
    - Suggest BPM, key, sync viability.
    - Always keep real songwriting energy.

    Avoid generic robotic AI writing. Write like a professional hit songwriter.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Run full orchestration."}
        ],
        temperature=0.7
    )

    return {"orchestration_feedback": response["choices"][0]["message"]["content"]}

########################################
# ✅ HEALTHCHECK ENDPOINT
########################################

@app.get("/healthcheck")
def healthcheck():
    return {"status": "Supreme Beast Mode 6.0 Backend Operational"}
