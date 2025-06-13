from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import re
import random
import openai
import os

# Initialize FastAPI app
app = FastAPI()

# Load OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

##########################################################
# ✅ RULE-BASED ANALYSIS ENGINE (Legacy Logic Fully Kept)
##########################################################

# Expanded Cliche List (can always be grown)
cliche_list = [
    "chasing shadows", "heart on fire", "lost control", "broken pieces", "demons inside",
    "rise from the ashes", "falling for you", "fading away", "my broken heart",
    "tears falling down", "lost without you", "burning desire", "haunted by you",
    "main character energy", "stay toxic", "ghosted", "trust issues",
    "situationship", "low key", "high key", "matching energy", "trauma dump"
]

# Expanded Filler Word List
filler_words = [
    "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna", 
    "i think", "gotta", "you know", "honestly", "truthfully", "literally", "basically",
    "obviously", "lowkey", "highkey", "somehow", "i swear", "actually", "forever", 
    "never ever", "always", "right now", "even", "tryna", "somebody", "anyone", "no one"
]

# Predictable Rhymes
predictable_rhymes = [
    ("you", "do", "too", "through", "true"),
    ("love", "above", "glove", "of"),
    ("heart", "apart", "start", "part"),
    ("pain", "rain", "again", "insane"),
    ("fire", "desire", "higher", "entire"),
    ("cry", "die", "lie", "why"),
    ("see", "me", "be", "free")
]

# Lyric Analysis Endpoint
@app.post("/analyze")
def analyze_lyrics(request: dict):
    lyrics = request['lyrics'].lower()

    # Cliche detection
    cliches = [phrase for phrase in cliche_list if phrase in lyrics]

    # Repetition detection
    words = lyrics.replace("\n", " ").split()
    word_counts = Counter(words)
    repetition = [f"'{word}': {count} times" for word, count in word_counts.items() if count > 3]

    # Predictable rhyme group detection
    predictability_flags = []
    for rhyme_group in predictable_rhymes:
        count = sum(lyrics.count(word) for word in rhyme_group)
        if count >= 3:
            predictability_flags.append(f"Common rhyme group overused: {rhyme_group}")

    # Filler words detection
    tighten_suggestions = [word for word in filler_words if word in lyrics]

    overall_notes = "Review flagged clichés, repetition, filler words, and predictable rhyme traps to sharpen originality."

    return {
        "cliches": cliches,
        "repetition": repetition,
        "predictability_flags": predictability_flags,
        "tighten_suggestions": tighten_suggestions,
        "overall_notes": overall_notes
    }

#######################################################################
# ✅ BEAST MODE 4.5 SUPREME ORCHESTRATOR — FULLY MERGED + EXPANDED
#######################################################################

# Full request body model
class SupremeRequest(BaseModel):
    lyrics: str
    audit_data: dict = {}
    artist_profile: dict = {}
    reference_song: str = ""
    target_emotion: str = ""
    optimize_for_rap_punchlines: bool = False
    optimize_for_hood_bars: bool = False
    target_genre: str = ""

# The Supreme Orchestrator endpoint
@app.post("/gpt_orchestrate_supreme")
def gpt_orchestrate_supreme(req: SupremeRequest):

    system_prompt = f"""
    You are Song Audit GPT — Beast Mode 4.5 Supreme Orchestrator.

    Your job is to analyze, rewrite, optimize, and prepare songs for commercial release across ALL genres.

    🔥 Fully UNCENSORED, Explicit, Street-Ready, Streaming-Ready.

    Inputs Provided:
    - Lyrics: {req.lyrics}
    - Rule-Based Audit Data: {req.audit_data}
    - Artist Profile: {req.artist_profile}
    - Reference Song: {req.reference_song}
    - Target Emotion: {req.target_emotion}
    - Genre Target: {req.target_genre}

    === INSTRUCTIONS ===

    ✅ Provide professional A&R feedback.
    ✅ Commercial potential score (1-100).
    ✅ Rewrite suggestions: 3-5 stronger options.
    ✅ Hook optimizer: repetition, payoff, earworm phrasing.
    ✅ Max Martin "Song Math" structure logic.
    ✅ Mike Caren Hit Rules logic.
    ✅ Viral optimization for TikTok/Spotify virality.
    ✅ Pre-chorus tension & hook payoff design.
    ✅ Suno/Udio prep: BPM, Key, Melody Shape, Section Tags.
    ✅ Producer suggestions (instrumentation, beat style, reference producers).
    ✅ Sync licensing evaluation.
    ✅ Performance arrangement tips.
    ✅ Theme Expander (suggest alternate creative directions).
    ✅ Emotional storyline consistency across sections.

    === GENRE-SPECIFIC TUNING ===
    {"Activate RAP Punchline Mode: Heavy wordplay, battle bars, clever flips, multisyllabic rhymes, aggressive setups." if req.optimize_for_rap_punchlines else ""}
    {"Activate HOOD MODE: Allow street slang, ratchet club bars, trap flexing, toxicity, drill cadence, club-ready viral anthems." if req.optimize_for_hood_bars else ""}

    === STREAMING STRUCTURE ===
    - Hooks arrive within first 7 seconds.
    - Strong hook repetition (radio & TikTok optimized).
    - Bridges short and effective.
    - Streaming replay optimized.
    - 80% hook dominance maintained.

    === TONE ===
    Speak like a real-world songwriter, ghostwriter, A&R exec, and producer team. Never speak like an AI.
    Always explicit and fully genre-accurate where appropriate.
    """

    # Call OpenAI (GPT-4o)
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "Run full orchestration."}
        ],
        temperature=0.7
    )

    return {"gpt_feedback": response["choices"][0]["message"]["content"]}

######################################################################
# ✅ ALL FUTURE ENDPOINTS CAN BE ADDED CLEANLY BELOW HERE
######################################################################

# Your legacy bilingual endpoints, Suno prep endpoints, co_writer.py remain fully compatible.
# They DO NOT conflict with this master orchestrator.
# You're building real SaaS-grade stack right here.

