from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import random

app = FastAPI()

# Input Models
class LyricsRequest(BaseModel):
    lyrics: str

class TrendRequest(BaseModel):
    phrase: str

class PredictabilityRequest(BaseModel):
    lyrics: str

class HookRequest(BaseModel):
    lyrics: str

class SyllableRequest(BaseModel):
    lyrics: str

class SurgeonRequest(BaseModel):
    lyrics: str

class VibeRequest(BaseModel):
    lyrics: str
    reference: str

class HookGenRequest(BaseModel):
    topic: str

class SectionRequest(BaseModel):
    lyrics: str

class TempoRequest(BaseModel):
    lyrics: str

class ChordRequest(BaseModel):
    lyrics: str

class ProductionRequest(BaseModel):
    lyrics: str

class HookAngleRequest(BaseModel):
    lyrics: str

class TrendDetectRequest(BaseModel):
    lyrics: str

class WriterLaneRequest(BaseModel):
    lyrics: str

class LyricVibeRequest(BaseModel):
    lyrics: str

class ThemeRequest(BaseModel):
    lyrics: str

class TitleRequest(BaseModel):
    lyrics: str

class GenRefRequest(BaseModel):
    lyrics: str
# Lyric Diagnostics - Ultra Expanded Anti-Mid Engine
@app.post("/analyze")
def analyze_lyrics(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    cliche_list = [
        # Expanded Cliché Library
        "chasing shadows", "heart on fire", "lost control", "i don’t chase i replace",
        "broken pieces", "demons inside", "rise from the ashes", "falling for you",
        "fading away", "my broken heart", "tears falling down", "darkness inside",
        "lost without you", "burning desire", "haunted by you", "you’re my everything",
        "take me higher", "drowning in your love", "written in the stars", "perfect storm",
        "crossroads ahead", "battle within", "piece of my heart", "shattered dreams",
        "eternally yours", "my destiny", "forever and always", "bleeding heart",
        "wasted time", "wasted love", "broken promises", "cold as ice", "lost cause",
        "he fumbled the bag", "level up", "move in silence", "glowed up", "stay toxic",
        "i'm him", "i'm her", "matching energy", "silent moves", "protecting my peace",
        "demon time", "ghosted", "left on read", "no new friends", "bossed up", "built different",
        "can't compete where you don't compare", "trust issues", "i gave you my all",
        "losing sleep over you", "can't live without you", "cold heart", "my heart can’t take this",
        "pain runs deep", "main character energy", "red flags", "situationship",
        "villain origin story", "soft launch", "low key", "high key", "trauma dump", "it's giving",
        "never good enough", "meant to be", "the one that got away", "forever yours",
        "falling apart", "haunted by your memory", "frozen heart", "broken inside",
        "alone again", "crashing down", "fall for you", "drifting apart", "torn apart",
        "second chance", "battle scars", "endless nights", "wasted love", "rollercoaster ride",
        "i upgraded", "boss energy", "dreams come true", "ride or die", "this is my era",
        "self made", "lost my way", "i surrender", "one more night", "can't lose you",
        "killing me softly", "time stands still", "heaven and hell", "light in the dark",
        "stormy weather", "empty inside", "you're my weakness", "i'm nothing without you"
    ]

    filler_words = [
        "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna", "i think",
        "gotta", "you know", "honestly", "truthfully", "so much", "literally", "basically",
        "obviously", "lowkey", "highkey", "somehow", "for you", "i swear", "actually", "especially",
        "somewhere", "something", "nothing much", "anything", "everything", "forever", "never ever",
        "always", "right now", "still", "always been", "still got", "even", "tryna", "all the way",
        "somebody", "no one", "anyone"
    ]

    predictable_rhymes = [
        ("you", "do", "too", "through", "blue", "true"),
        ("love", "above", "glove", "of", "enough", "tough"),
        ("night", "light", "fight", "alright", "bright", "tonight", "might"),
        ("heart", "apart", "start", "part", "chart", "smart"),
        ("pain", "rain", "again", "insane", "brain", "vein"),
        ("fire", "desire", "higher", "wire", "entire"),
        ("cry", "die", "goodbye", "lie", "why", "high"),
        ("see", "me", "be", "free", "we", "agree", "guarantee"),
        ("fall", "call", "all", "wall", "small", "stall"),
        ("alone", "phone", "home", "known", "gone", "stone", "throne"),
        ("time", "mine", "shine", "line", "fine", "divine", "decline"),
        ("way", "stay", "play", "day", "say", "away", "today"),
        ("girl", "world", "whirl", "pearl", "twirl"),
        ("boy", "joy", "destroy", "deploy"),
        ("life", "strife", "knife", "wife"),
        ("hold", "cold", "told", "sold", "bold", "unfold")
    ]

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
# Trend Tracker
@app.post("/trendcheck")
def trend_check(request: TrendRequest):
    trending_terms = [
        "delulu", "rizz", "girl dinner", "situationship", "npc", "main character energy",
        "core memory", "it's giving", "glowed up", "soft launch", "no cap", "bussin",
        "caught a vibe", "stay toxic", "trauma dump", "plot armor", "gaslight", "fumbled the bag",
        "lowkey", "highkey", "mood swings", "energy shift", "outside but dead inside",
        "slow burn", "era", "i ate", "ratio", "deadass", "smash or pass", "grwm", "stan"
    ]
    trending = request.phrase.lower() in [term.lower() for term in trending_terms]
    return {"phrase": request.phrase, "is_trending": trending}

# Predictability Score - Expanded Triggers
@app.post("/predictability")
def predictability_score(request: PredictabilityRequest):
    lyrics = request.lyrics.lower()
    triggers = [
        "heart", "love", "pain", "cry", "baby", "maybe", "forever", "always", "you", "true",
        "broken", "gone", "lost", "tears", "regret", "lonely", "missing", "drowning", "empty",
        "surrender", "wasted", "addicted", "falling apart", "frozen", "shattered", "nightmare",
        "demon", "ghosted", "villain", "can't breathe", "complete me", "fate", "written in the stars",
        "endless nights", "walls closing in", "heaven and hell", "silent moves", "protecting my peace",
        "stay toxic", "glowed up", "built different", "matching energy", "unbothered", "energy shift"
    ]
    score = 50 + sum(lyrics.count(word) for word in triggers)
    score = min(score, 100)
    return {"predictability_score": score}

# Hook Strength Analyzer
@app.post("/hookcheck")
def hook_check(request: HookRequest):
    lyrics = request.lyrics
    word_count = len(lyrics.split())
    chantable = any(word in lyrics.lower() for word in ["oh", "yeah", "uh", "na", "la"])
    viral = word_count <= 20 and chantable
    return {"hook_strength": "Strong viral hook potential" if viral else "Could be tighter for streaming."}

# Syllable Mapper
@app.post("/syllablemap")
def syllable_map(request: SyllableRequest):
    lyrics = request.lyrics.split("\n")
    results = []
    for line in lyrics:
        syllables = sum(1 for char in line if char.lower() in "aeiouy")
        results.append({"line": line, "syllables": syllables})
    return {"syllable_map": results}

# Lyrical Surgeon
@app.post("/lyricalsurgeon")
def lyrical_surgeon(request: SurgeonRequest):
    lyrics = request.lyrics
    replacements = [
        ("falling apart", "breaking down"), ("broken heart", "shattered heart"),
        ("lost control", "spinning out"), ("can't breathe", "suffocating"),
        ("you complete me", "you uplift me"), ("written in the stars", "fate collided"),
        ("fading away", "slipping under"), ("holding on", "barely hanging")
    ]
    improved = lyrics
    for old, new in replacements:
        improved = improved.replace(old, new)
    return {"original": lyrics, "suggested_rewrite": improved}

# Vibe Matcher — Expanded artist clusters (simplified)
@app.post("/vibematch")
def vibe_match(request: VibeRequest):
    vibe_clusters = {
        "drake": "Late night flex / Emotional vulnerability",
        "sza": "Toxic situationship / Healing / Self-worth",
        "post malone": "Fame pain / Regret / Escape vibes",
        "brent faiyaz": "Toxic intimacy / Withdrawal",
        "summer walker": "Trust issues / Insecurity / Rebuilding",
        "future": "Toxic flex / Unbothered / Demon time",
        "the weeknd": "Obsessive love / Vices / After hours",
        "doja cat": "Confidence / Boss energy / Playful",
        "billie eilish": "Isolation / Depression / Vulnerability",
        "metro boomin": "Dark trap / Moody energy",
        "olivia rodrigo": "Teen heartbreak / Emotional honesty",
        "bad bunny": "Party / Latin Trap / Smooth flex",
        "ice spice": "Viral playful bars / Unbothered glow up",
        "21 savage": "Street monotone flex / Cold delivery",
        "bruno mars": "Retro funk / Romantic serenade",
        "beyonce": "Empowerment / Female dominance",
        "rihanna": "Confidence / Toxic independence",
        "frank ocean": "Melancholy / Abstract emotion",
        "giveon": "Heartbreak / Soul R&B pain",
        "taylor swift": "Storytelling / Relationship analysis"
    }
    reference = request.reference.lower()
    vibe = vibe_clusters.get(reference, "No direct match found — GPT expansion recommended.")
    return {"vibe_reference": reference, "vibe_profile": vibe}

# Lyric Vibe Profiler
@app.post("/lyricvibe")
def lyric_vibe(request: LyricVibeRequest):
    lyrics = request.lyrics.lower()
    if "toxic" in lyrics or "energy" in lyrics:
        vibe = "Modern toxic R&B"
    elif "cry" in lyrics or "alone" in lyrics:
        vibe = "Sad ballad / breakup"
    elif "flex" in lyrics or "money" in lyrics:
        vibe = "Trap flex anthem"
    else:
        vibe = "General emotional pop"
    return {"lyric_vibe": vibe}

# Title Generator
@app.post("/titlegen")
def title_gen(request: TitleRequest):
    titles = ["Lost Again", "No More Chances", "Cold Like December", "Toxic Love", "Midnight Fade", "Better Without You"]
    return {"generated_titles": random.sample(titles, 3)}

# Theme Generator
@app.post("/themegen")
def theme_gen(request: ThemeRequest):
    themes = ["Heartbreak", "Glow up", "Toxic love", "Comeback story", "Unbothered energy", "Late night thoughts"]
    return {"generated_themes": random.sample(themes, 3)}

# Hook Generator
@app.post("/hookgen")
def hook_generator(request: HookGenRequest):
    topic = request.topic
    hooks = [
        f"{topic} got me losing sleep again",
        f"All I need is {topic} tonight",
        f"Can't let go of this {topic}",
        f"Falling deeper into {topic}",
        f"This {topic} got my head spinning"
    ]
    return {"generated_hooks": hooks}

# Section Classifier
@app.post("/classifysections")
def classify_sections(request: SectionRequest):
    lyrics = request.lyrics.lower()
    sections = {
        "hook": any(word in lyrics for word in ["chorus", "hook", "repeat", "all i need", "falling for you"]),
        "bridge": any(word in lyrics for word in ["bridge", "breakdown", "build"]),
        "verse": any(word in lyrics for word in ["verse", "story", "line", "verse 1", "verse 2"])
    }
    return {"sections_detected": sections}

# Tempo Suggestion
@app.post("/temposuggest")
def tempo_suggest(request: TempoRequest):
    lyrics = request.lyrics.lower()
    if any(word in lyrics for word in ["club", "dance", "party", "move", "shake"]):
        bpm = random.randint(100, 130)
        mood = "High energy / Club"
    elif any(word in lyrics for word in ["cry", "alone", "slow", "pain", "sad"]):
        bpm = random.randint(60, 80)
        mood = "Emotional / Ballad"
    else:
        bpm = random.randint(80, 100)
        mood = "Mid-tempo / Chill"
    return {"bpm_suggestion": bpm, "mood": mood}

# Chord Progression Generator
@app.post("/chordsuggest")
def chord_suggest(request: ChordRequest):
    progressions = [
        "I - V - vi - IV", "vi - IV - I - V", "ii - V - I - vi", "I - vi - IV - V",
        "i - VI - III - VII", "i - iv - V - i"
    ]
    return {"suggested_progressions": random.sample(progressions, 3)}

# Production Suggestion
@app.post("/productionsuggest")
def production_suggest(request: ProductionRequest):
    styles = ["Trap hats", "808 bounce", "Lofi drums", "Dark pads", "Synth plucks", "Ambient layers"]
    energy = ["Minimal chill", "Dark emotional", "Club banger", "TikTok viral friendly", "Radio-ready", "Acoustic intimate"]
    return {
        "production_styles": random.sample(styles, 3),
        "energy_suggestions": random.sample(energy, 2)
    }

# Hook Angle Generator
@app.post("/hookangles")
def hook_angles(request: HookAngleRequest):
    topics = ["toxic cycles", "trust issues", "self love", "fame struggles", "late night texts", "moving on"]
    return {"hook_angles": random.sample(topics, 3)}

# Sound Trend Detector
@app.post("/trenddetector")
def trend_detector(request: TrendDetectRequest):
    trends = ["TikTok loops", "Alt-R&B", "Trap soul", "Bedroom pop", "Post-Drake sad rap", "Indie viral sound"]
    return {"current_trends": trends}

# Writer Lane Coach
@app.post("/writerlane")
def writer_lane(request: WriterLaneRequest):
    lanes = ["Streaming Hit", "TikTok Viral", "Radio Crossover", "Deep Album Cut", "Sync Licensing"]
    return {"recommended_lanes": random.sample(lanes, 2)}

# Generational Reference Matcher
@app.post("/genreference")
def genreference(request: GenRefRequest):
    eras = [
        "80s Synth Pop", "90s R&B Heartbreak", "70s Funk Grooves", 
        "60s Motown Soul", "Early 2000s Crunk", "2010s Trap Wave"
    ]
    return {"generational_references": random.sample(eras, 3)}
