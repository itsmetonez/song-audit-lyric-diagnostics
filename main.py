from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter
import random
import re

app = FastAPI()

# INPUT MODELS (this supports both lyric and Suno/Udio modes)
class LyricsRequest(BaseModel):
    lyrics: str

class SunoRequest(BaseModel):
    lyrics: str
    section_tags: list
    bpm: int = None
    key: str = None

class FeedbackRequest(BaseModel):
    feedback: str

class ModeRequest(BaseModel):
    mode: str  # "lyrics" or "suno"

# MASTER CLICHÉ LIST (shortened for part 1 - full expanded list coming in next drops)
cliche_list = [
    "chasing shadows", "heart on fire", "lost control", "i don’t chase i replace",
    "broken pieces", "demons inside", "rise from the ashes", "falling for you",
    "fading away", "my broken heart", "tears falling down", "darkness inside",
    "lost without you", "burning desire", "haunted by you", "you're my everything",
    "main character energy", "villain origin story", "stay toxic", "trust issues",
    "ghosted", "no new friends", "situationship", "low key", "high key",
    "matching energy", "trauma dump", "he fumbled the bag", "built different"
]

# MASSIVE FILLER WORD LIST (expanded fully in Part 2)
filler_words = [
    "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna", "i think",
    "gotta", "you know", "honestly", "truthfully", "literally", "basically",
    "obviously", "lowkey", "highkey", "somehow", "for you", "i swear", "actually", 
    "especially", "forever", "never ever", "always", "right now", "even", "tryna",
    "somebody", "anyone", "no one"
]

# PREDICTABLE RHYMES (more expansion in Part 2)
predictable_rhymes = [
    ("you", "do", "too", "through", "true"),
    ("love", "above", "glove", "of"),
    ("heart", "apart", "start", "part"),
    ("pain", "rain", "again", "insane"),
    ("fire", "desire", "higher", "entire"),
    ("cry", "die", "lie", "why"),
    ("see", "me", "be", "free"),
]

# PROFANITY FILTER
def clean_profanity(lyrics):
    censor_map = {
        "fuck": "f*%k",
        "shit": "sh*%",
        "bitch": "b*%ch",
        "ass": "a$%",
        "nigga": "n*%ga",
        "dick": "d*%k",
        "pussy": "p*%sy",
        "hoe": "h*%",
        "slut": "s*%t"
    }
    for bad, censored in censor_map.items():
        lyrics = re.sub(rf'\b{bad}\b', censored, lyrics, flags=re.IGNORECASE)
    return lyrics
# FULL EXPANDED LYRICS ENGINE MODULE

# MASSIVE CLICHÉ LIST (expanded heavily)
cliche_list = [
    "chasing shadows", "heart on fire", "lost control", "i don’t chase i replace",
    "broken pieces", "demons inside", "rise from the ashes", "falling for you",
    "fading away", "my broken heart", "tears falling down", "darkness inside",
    "lost without you", "burning desire", "haunted by you", "you're my everything",
    "take me higher", "drowning in your love", "perfect storm", "battle within",
    "piece of my heart", "shattered dreams", "eternally yours", "forever and always",
    "wasted love", "broken promises", "cold as ice", "lost cause", "he fumbled the bag",
    "move in silence", "glowed up", "stay toxic", "matching energy", "silent moves",
    "protecting my peace", "demon time", "ghosted", "left on read", "no new friends",
    "built different", "trust issues", "losing sleep over you", "cold heart", 
    "main character energy", "red flags", "villain origin story", "soft launch", 
    "low key", "high key", "trauma dump", "it's giving", "never good enough", 
    "the one that got away", "falling apart", "frozen heart", "drifting apart",
    "second chance", "battle scars", "rollercoaster ride", "i upgraded", 
    "boss energy", "ride or die", "this is my era", "self made", "lost my way", 
    "killing me softly", "time stands still", "heaven and hell", "stormy weather", 
    "empty inside", "you're my weakness", "i'm nothing without you", 
    "broke my heart again", "don't need no man", "did it for the plot", 
    "for the culture", "mood swings", "outside but dead inside", "energy shift",
    "slow burn", "plot armor", "ratio", "delulu", "npc", "girl dinner", "bussin",
    "caught a vibe", "gaslight", "deadass", "smash or pass", "grwm", "stan"
]

# MASSIVE FILLER WORD LIST (fully expanded)
filler_words = [
    "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna", 
    "i think", "gotta", "you know", "honestly", "truthfully", "so much", "literally", 
    "basically", "obviously", "lowkey", "highkey", "somehow", "for you", "i swear", 
    "actually", "especially", "somewhere", "something", "nothing much", "anything", 
    "everything", "forever", "never ever", "always", "right now", "still", "always been", 
    "still got", "even", "tryna", "all the way", "somebody", "no one", "anyone",
    "every time", "always had", "honestly speaking", "deep down", "truly", "pretty much", 
    "kind of", "sort of", "totally", "completely", "absolutely", "seriously", "exactly",
    "eventually", "definitely", "probably", "maybe someday", "literally dying", 
    "to be honest", "if i’m being real", "low key vibe", "high key flex", 
    "kinda sorta", "i feel like", "not gonna lie"
]

# EXPANDED PREDICTABLE RHYMES
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

# THE FULL LYRICS ANALYSIS FUNCTION
@app.post("/analyze")
def analyze_lyrics(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # Cliché Detector
    cliches = [phrase for phrase in cliche_list if phrase in lyrics]

    # Repetition Detector
    words = lyrics.replace("\n", " ").split()
    word_counts = Counter(words)
    repetition = [f"'{word}': {count} times" for word, count in word_counts.items() if count > 3]

    # Predictable Rhymes Detector
    predictability_flags = []
    for rhyme_group in predictable_rhymes:
        count = sum(lyrics.count(word) for word in rhyme_group)
        if count >= 3:
            predictability_flags.append(f"Common rhyme group overused: {rhyme_group}")

    # Filler Word Detector
    tighten_suggestions = [word for word in filler_words if word in lyrics]

    # Final Notes
    overall_notes = "Review flagged clichés, repetition, filler words, and predictable rhyme traps to sharpen originality."

    return {
        "cliches": cliches,
        "repetition": repetition,
        "predictability_flags": predictability_flags,
        "tighten_suggestions": tighten_suggestions,
        "overall_notes": overall_notes
    }
# SUNO/UDIO PRODUCTION PROMPT ENGINE

@app.post("/generate_prompt")
def generate_prompt(request: LyricsRequest):

    lyrics = request.lyrics

    # Extract all the section headers in [ ] brackets
    section_headers = re.findall(r"\[(.*?)\]", lyrics)

    # Build list of tags & descriptors based on user [ ] tags
    tag_list = []
    for header in section_headers:
        split_tags = [t.strip().lower() for t in header.split(",")]
        tag_list.extend(split_tags)

    # Safety dedupe
    tag_list = list(set(tag_list))

    # Genre Prediction Logic (simplified)
    if any(tag in tag_list for tag in ["trap", "rap", "atlanta", "hood", "club", "anthemic", "tiktok"]):
        genre = "Trap / Hip-Hop / Streaming Viral"
    elif any(tag in tag_list for tag in ["afrobeat", "afrobeats", "afro pop"]):
        genre = "Afrobeats"
    elif any(tag in tag_list for tag in ["brazilian", "funk", "carioca", "boi-bumba", "toada"]):
        genre = "Brazilian Funk / Amazonian Pop"
    elif any(tag in tag_list for tag in ["r&b", "rnb", "emotional", "soul", "slow burn"]):
        genre = "Pop / R&B Crossover"
    elif any(tag in tag_list for tag in ["edm", "dance", "club banger", "festival"]):
        genre = "EDM / Dance"
    elif any(tag in tag_list for tag in ["latin", "reggaeton", "spanish", "bilingual"]):
        genre = "Latin / Reggaeton / Bilingual"
    else:
        genre = "Modern Pop / Top 40"

    # Tempo Estimation Logic
    if "slow burn" in tag_list or "ballad" in tag_list or "sad" in tag_list:
        tempo = random.randint(65, 85)
    elif "club" in tag_list or "tiktok" in tag_list or "anthemic" in tag_list:
        tempo = random.randint(105, 125)
    elif "brazilian" in tag_list or "funk" in tag_list:
        tempo = random.randint(115, 125)
    else:
        tempo = random.randint(80, 100)

    # Inject TikTok-friendly tag logic
    if any(tag in tag_list for tag in ["tiktok", "chant", "viral", "anthemic", "streaming"]):
        tiktok_phrase = "This arrangement is highly TikTok and streaming-friendly with chantable hooks and viral topline."
    else:
        tiktok_phrase = ""

    # Inject bilingual logic
    if "bilingual" in tag_list:
        language_phrase = "Blending bilingual phrasing with explosive call-and-response energy."
    else:
        language_phrase = ""

    # Build final production prompt
    prompt = (
        f"This {genre} track opens with vibes reflecting {', '.join(tag_list)}. "
        f"{language_phrase} "
        f"{tiktok_phrase} "
        f"Expect dynamic production with stacked harmonies, adlibs, vocal layering, {genre.lower()} rhythmic textures, and streaming-optimized transitions. "
        f"Estimated BPM: {tempo}."
    )

    return {"generated_production_prompt": prompt}
# FULL PROFANITY FILTER MODULE (EXPANDED)

def clean_profanity(lyrics):
    censor_map = {
        "fuck": "f*%k", "fucking": "f*%king", "motherfucker": "motherf*%ker",
        "shit": "sh*%", "bullshit": "bullsh*%", "bastard": "b*%tard",
        "bitch": "b*%ch", "bitches": "b*%ches",
        "ass": "a$%", "asshole": "a$%hole", "dumbass": "dumba$%",
        "nigga": "n*%ga", "nigger": "n*%gger", "niggaz": "n*%gaz",
        "dick": "d*%k", "dicks": "d*%ks",
        "pussy": "p*%sy", "pussies": "p*%sies",
        "hoe": "h*%", "hoes": "h*%s",
        "slut": "s*%t", "sluts": "s*%ts",
        "cunt": "c*%t", "fag": "f*%", "faggot": "f*%got",
        "retard": "re*%ard", "retarded": "re*%arded"
    }

    for bad, censored in censor_map.items():
        pattern = re.compile(rf"\b{bad}\b", re.IGNORECASE)
        lyrics = pattern.sub(censored, lyrics)
    return lyrics
# A&R LABEL READINESS MODULE

@app.post("/label_readiness")
def label_readiness(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    score = 50

    # Boost for strong structure
    if "[chorus" in lyrics and "[verse" in lyrics:
        score += 10

    # Deduct for clichés
    cliche_count = sum(lyrics.count(phrase) for phrase in cliche_list)
    score -= min(cliche_count * 2, 15)

    # Deduct for filler
    filler_count = sum(lyrics.count(word) for word in filler_words)
    score -= min(filler_count * 2, 10)

    # Deduct for repetition
    words = lyrics.replace("\n", " ").split()
    word_counts = Counter(words)
    repetition_count = sum(1 for count in word_counts.values() if count >= 5)
    score -= min(repetition_count * 2, 10)

    # Deduct for rhyme traps
    rhyme_flags = 0
    for rhyme_group in predictable_rhymes:
        count = sum(lyrics.count(word) for word in rhyme_group)
        if count >= 3:
            rhyme_flags += 1
    score -= min(rhyme_flags * 3, 10)

    # Clamp score between 0-100
    final_score = max(min(score, 100), 0)

    # Label tier assessment
    if final_score >= 85:
        tier = "Label Ready 🔥"
    elif final_score >= 70:
        tier = "Very Strong - Commercial Potential"
    elif final_score >= 50:
        tier = "Decent Foundation - Needs Development"
    else:
        tier = "Early Draft - Needs Work"

    return {
        "label_readiness_score": final_score,
        "readiness_tier": tier
    }
# PRE-SESSION IDEA GENERATOR + WRITER LANE MODULE

@app.post("/presession_ideas")
def pre_session_ideas():
    themes = [
        "Heartbreak recovery", "Toxic love cycles", "Late night flexing",
        "Main character energy", "Rebuilding self-worth", "Trust issues & vulnerability",
        "Loneliness masked by confidence", "Moving on from situationships",
        "Craving attention vs. protecting peace", "Self-sabotage in love",
        "Chasing validation", "Jealousy and competition", 
        "Unbothered glow-up era", "Hidden insecurities behind confidence",
        "Revenge flex anthem", "Forbidden chemistry", "Love vs. career sacrifice"
    ]

    hook_angles = [
        "Toxic cycles I keep running back to",
        "Glow up after getting ghosted",
        "Flexing while secretly broken inside",
        "Tension between vulnerability and ego",
        "Revenge anthem after betrayal",
        "Building confidence after heartbreak",
        "Hook-up culture fatigue",
        "Diving into something forbidden",
        "Career grind over love"
    ]

    return {
        "session_themes": random.sample(themes, 5),
        "hook_angle_ideas": random.sample(hook_angles, 3)
    }

# WRITER LANE COACH (Placement Targeting)
@app.post("/writer_lane")
def writer_lane():
    lanes = [
        "Streaming Hit (Spotify, Apple)", 
        "TikTok Viral Potential", 
        "Radio Crossover", 
        "Deep Album Cut", 
        "Sync Licensing (TV/Film/Ads)"
    ]
    return {
        "recommended_lanes": random.sample(lanes, 2)
    }
# REGIONAL STYLE + GENERATIONAL REFERENCES + CHORD SUGGESTION MODULE

# GENERATIONAL REFERENCE
@app.post("/generational_reference")
def generational_reference():
    eras = [
        "80s Synth Pop", "90s R&B Heartbreak", "70s Funk Grooves", 
        "60s Motown Soul", "Early 2000s Crunk", "2010s Trap Wave",
        "Afrobeats Rise 2020s", "Latin Pop Crossover 2020s", 
        "Atlanta Trap Movement", "Nashville Modern Country"
    ]
    return {"generational_references": random.sample(eras, 3)}

# SOUND TREND DETECTOR
@app.post("/trend_detector")
def trend_detector():
    trends = [
        "TikTok loops", "Alt-R&B", "Trap soul", "Bedroom pop", 
        "Post-Drake sad rap", "Indie viral sound", 
        "Afro-Pop Streaming Wave", "Brazilian Funk Explosion",
        "Arabic Trap Crossovers", "Reggaeton Global Chart Dominance"
    ]
    return {"current_trends": random.sample(trends, 3)}

# CHORD PROGRESSION GENERATOR
@app.post("/chord_suggestion")
def chord_suggestion():
    progressions = [
        "I - V - vi - IV", "vi - IV - I - V", "ii - V - I - vi", "I - vi - IV - V",
        "i - VI - III - VII", "i - iv - V - i",
        "vi - I - IV - V", "I - iii - IV - V", "I - IV - ii - V"
    ]
    return {"suggested_progressions": random.sample(progressions, 3)}
# CONVERSATIONAL LOGIC + CREATOR CREDIT + FEEDBACK HANDLER

@app.post("/about")
def about_you():
    capabilities = """
Here’s what I can do:

🎯 Lyric Analysis (anti-cliché, predictability, repetition, hook strength, A&R label readiness)
🎯 Song Structure Assistant (sections, syllables, writer lane targeting)
🎯 Hook + Title + Theme Generator
🎯 Chord, Tempo, Production Suggestion
🎯 Generational References + Streaming Lane Targeting
🎯 Pre-Session Idea Assistant
🎯 Profanity Cleaner (for OpenAI compliance)
🎯 Suno/Udio Full Production Prompt Generator (using your lyrics + tags)
🎯 Genre-aware, region-aware, and arrangement-aware production blueprints
🎯 Key + Tempo Assistant for uploaded tracks
🎯 Session-ready AI writing assistant
🎯 Streaming Optimization / Viral Writing Focus
🎯 Full A&R Assistant
🎯 Real-time AI Co-Writing Assistant

🔧 Who built me?
Song Audit was built and fine-tuned by Tony Ghantous @itsmetonez ❤️ 
His production company is The MoonTonez. 
IG: instagram.com/itsmetonez 
He engineered me to help for solo and session writing, and give songwriters a virtual co-writer that speaks the modern hit language, and is more curated than regular GPT!

💡 Feedback? Suggestions?
I’m always improving based on real user input.
👉 DM Tony directly on IG at @itsmetonez with feature requests, ideas or feedback.
"""
    return {"about": capabilities}

# Simple keyword triggers for friendly convo (simulating frontend logic)
@app.post("/handle_question")
def handle_question(request: FeedbackRequest):
    user_input = request.feedback.lower()

    trigger_words = ["who built you", "what can you do", "tell me more", "feedback", "suggestions"]

    if any(trigger in user_input for trigger in trigger_words):
        return about_you()
    else:
        return {"response": "I'm here! Drop your lyrics or request anytime 🔥"}

# Friendly chat starter endpoint
@app.post("/start_session")
def start_session():
    welcome = (
# INTERPOLATION & SONG FLIP ASSISTANT MODULE

@app.post("/interpolation_flip")
def interpolation_flip(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # Genre / Era Banks to flip
    eras = [
        "80s Synthwave", "90s R&B", "2000s Crunk", 
        "2010s Trap", "2000s Pop Punk", "70s Soul", 
        "90s Alternative Rock", "Classic Reggaeton", 
        "UK Garage", "Afrobeats 2020s", "Latin Urban"
    ]

    vibe_flips = [
        "Turn this into a stripped down acoustic ballad.",
        "Flip into an uptempo club anthem.",
        "Reimagine with nostalgic 90s R&B flavor.",
        "Rework into Afrobeat crossovers.",
        "Flip as TikTok-friendly viral loop.",
        "Transform into a Latin Urban crossover.",
        "Flip as a male/female duet version.",
        "Turn into a cinematic ballad for sync licensing.",
        "Rework into trap soul mood with modern 808s.",
        "Make this fit a 'Main Character Energy' glow-up vibe.",
        "Flip into a throwback pop-funk groove."
    ]

    # Logic for some light lyric-based genre triggers
    genre_flips = []
    if any(word in lyrics for word in ["flex", "money", "trap", "chains", "ice"]):
        genre_flips.append("Flip into a melodic emo trap vibe with heavy 808s.")
    if any(word in lyrics for word in ["heartbreak", "cry", "pain", "tears", "alone"]):
        genre_flips.append("Flip into sad girl R&B with haunting harmonies.")
    if any(word in lyrics for word in ["club", "dance", "move", "party"]):
        genre_flips.append("Flip into a high energy festival EDM crossover.")

    return {
        "interpolation_flip_ideas": random.sample(vibe_flips, 3),
        "era_flip_suggestions": random.sample(eras, 3),
        "genre_flip_triggers": genre_flips
    }
# SONG MATH ENGINE — SECTION VALIDATOR MODULE

@app.post("/song_math")
def song_math(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # Count measures inside sections
    sections = re.findall(r"\[(.*?)\]", lyrics)
    section_lengths = {}

    for sec in sections:
        # Try to extract measure counts from tag
        match = re.search(r'(\d+)\s*measures?', sec)
        if match:
            count = int(match.group(1))
            section_name = sec.split(",")[0].strip().lower()
            section_lengths[section_name] = count

    # Default healthy range for sections (industry rule of thumb)
    section_targets = {
        "intro": (2, 8),
        "verse": (8, 16),
        "pre-chorus": (4, 8),
        "chorus": (8, 16),
        "post-chorus": (4, 8),
        "bridge": (4, 8),
        "outro": (2, 8)
    }

    notes = []
    for section, measures in section_lengths.items():
        for target_sec, (min_val, max_val) in section_targets.items():
            if target_sec in section:
                if measures < min_val:
                    notes.append(f"{section.title()} may feel rushed — consider expanding to at least {min_val} measures.")
                elif measures > max_val:
                    notes.append(f"{section.title()} may run long — could trim closer to {max_val} measures for better pacing.")

    if not section_lengths:
        notes.append("⚠ No measure counts detected. Try adding tags like [Chorus, 8 measures] for Song Math feedback.")

    return {
        "section_length_flags": notes
    }
# STREAMING OPTIMIZER ENGINE — RETENTION RULES MODULE

@app.post("/streaming_optimizer")
def streaming_optimizer(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    feedback = []

    # Simulated clock timing based on typical section measure assumptions
    section_times = {
        "intro": 5,  # assume ~5 sec
        "verse": 15,  # ~15 sec per verse section
        "pre-chorus": 7, 
        "chorus": 10,
        "post-chorus": 7,
        "bridge": 10,
        "outro": 5
    }

    # Simplified estimator: sum total section time
    sections = re.findall(r"\[(.*?)\]", lyrics)
    total_time = 0
    first_chorus_time = None

    for sec in sections:
        sec_lower = sec.lower()
        for key, est_time in section_times.items():
            if key in sec_lower:
                total_time += est_time
                if "chorus" in sec_lower and first_chorus_time is None:
                    first_chorus_time = total_time

    # Streaming-era retention checks
    if first_chorus_time and first_chorus_time > 45:
        feedback.append("⚠ First chorus may arrive late (after 45s). Try pulling your hook sooner to reduce early skips.")

    if total_time > 180:
        feedback.append("⚠ Total song length may exceed ideal streaming time (3:00). Consider trimming for better replay value.")

    if total_time < 120:
        feedback.append("⚠ Total song length may be too short for platform algorithms (under 2:00).")

    if not first_chorus_time:
        feedback.append("⚠ No chorus detected. Make sure your hook arrives within first 30-45 seconds for streaming.")

    return {
        "streaming_retention_feedback": feedback
    }
# VIRAL MAXIMIZER — TIKTOK & CHANTABILITY BOOSTER MODULE

@app.post("/viral_maximizer")
def viral_maximizer(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    chant_words = [
        "oh", "yeah", "uh", "na", "la", "hey", "woo", "skrrt", "aye", 
        "let's go", "okay", "alright", "turn up", "run it back", "vibe", 
        "gang", "flex", "drip", "ice", "repeat", "again", "lit"
    ]

    viral_flags = []
    chant_count = sum(lyrics.count(word) for word in chant_words)

    # Chantable threshold logic
    if chant_count >= 5:
        viral_flags.append("🔥 Strong chantable hook density detected — highly viral for TikTok loop potential.")
    elif chant_count >= 2:
        viral_flags.append("🟡 Decent chant repetition — consider boosting hook callouts for stronger viral pull.")
    else:
        viral_flags.append("⚠ Low chantable phrases — adding repeatable hook words may increase viral replay.")

    # Hook repetition suggestions
    hook_repeats = re.findall(r"\b(chorus|hook)\b", lyrics)
    if len(hook_repeats) >= 3:
        viral_flags.append("🔥 Excellent hook repetition for TikTok catchiness.")
    elif len(hook_repeats) == 0:
        viral_flags.append("⚠ Consider inserting more visible hook sections for viral retention.")

    return {
        "viral_maximizer_feedback": viral_flags
    }
# HOOK IMPACT ANALYZER — FIRST 30 SEC HIT TEST

@app.post("/hook_impact")
def hook_impact(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # Slice first ~4 sections as proxy for first 30s (assumes standard pacing)
    sections = re.findall(r"\[(.*?)\]", lyrics)
    first_sections = sections[:4]

    hook_score = 0
    hook_detected = False

    for sec in first_sections:
        sec_lower = sec.lower()
        if "chorus" in sec_lower or "hook" in sec_lower:
            hook_detected = True
            hook_score += 20

        if any(word in sec_lower for word in ["chant", "catchy", "viral", "tiktok", "anthemic"]):
            hook_score += 10

        if any(word in sec_lower for word in ["repeat", "singalong", "call and response", "stacked vocals"]):
            hook_score += 5

    if hook_detected and hook_score >= 30:
        feedback = "🔥 Excellent early hook impact — strong first 30s for streaming retention."
    elif hook_detected:
        feedback = "🟡 Hook arrives early — consider boosting hook density for stronger viral pull."
    else:
        feedback = "⚠ No hook detected in first 30s — high skip risk for streaming algorithms."

    return {
        "hook_impact_feedback": feedback
    }
# ARRANGEMENT VALIDATOR MODULE — SECTION BALANCE CHECK

@app.post("/arrangement_validator")
def arrangement_validator(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    sections = re.findall(r"\[(.*?)\]", lyrics)
    
    pre_count = sum(1 for sec in sections if "pre-chorus" in sec.lower())
    bridge_count = sum(1 for sec in sections if "bridge" in sec.lower())
    post_count = sum(1 for sec in sections if "post-chorus" in sec.lower())

    arrangement_flags = []

    # Pre-Chorus Logic
    if pre_count == 0:
        arrangement_flags.append("⚠ No pre-chorus detected — adding one may improve tension into the hook.")
    elif pre_count > 2:
        arrangement_flags.append("🟡 Multiple pre-choruses detected — ensure pacing stays tight.")

    # Bridge Logic
    if bridge_count == 0:
        arrangement_flags.append("⚠ No bridge detected — consider adding a bridge to break up repetition.")
    elif bridge_count > 1:
        arrangement_flags.append("🟡 Multiple bridges — verify emotional build remains dynamic.")

    # Post-Chorus Logic
    if post_count == 0:
        arrangement_flags.append("⚠ No post-chorus — adding one may help viral replay strength.")
    elif post_count >= 2:
        arrangement_flags.append("🟡 Multiple post-choruses — check for over-repetition.")

    if not arrangement_flags:
        arrangement_flags.append("✅ Section balance looks healthy for streaming-first structure.")

    return {
        "arrangement_feedback": arrangement_flags
    }
# KEY & BPM FINDER ASSISTANT MODULE

@app.post("/key_bpm_assist")
def key_bpm_assist(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # Simplified smart genre prediction from tags (used if user doesn't know key or BPM)
    genre_hints = {
        "trap": ("C minor", 140),
        "r&b": ("G minor", 90),
        "pop": ("C major", 100),
        "edm": ("F minor", 125),
        "latin": ("A minor", 105),
        "afrobeats": ("E major", 100),
        "brazilian": ("D minor", 115),
        "funk": ("G minor", 110),
        "arabic": ("D harmonic minor", 95)
    }

    default_key = "C major"
    default_bpm = 100

    detected_key = default_key
    detected_bpm = default_bpm

    # Scan your section tags for genre triggers
    sections = re.findall(r"\[(.*?)\]", lyrics)
    tags = []
    for sec in sections:
        tags.extend([t.strip().lower() for t in sec.split(",")])

    for genre, (k, bpm) in genre_hints.items():
        if any(genre in tag for tag in tags):
            detected_key = k
            detected_bpm = bpm

    return {
        "predicted_key": detected_key,
        "predicted_bpm": detected_bpm,
        "note": "If you're uploading your own track, you can override these with your actual key and tempo."
    }
# MASTER A&R FEEDBACK AGGREGATOR — FULL SESSION SUMMARY MODULE

@app.post("/full_audit")
def full_audit(request: LyricsRequest):
    lyrics = request.lyrics

    # Call each module manually (modular approach for stacking your engine)
    interpolation = interpolation_flip(request)
    songmath = song_math(request)
    streaming = streaming_optimizer(request)
    viral = viral_maximizer(request)
    hooktest = hook_impact(request)
    arrangement = arrangement_validator(request)
    keybpm = key_bpm_assist(request)

    # Aggregate feedback summary
    return {
        "Interpolation_Flip_Ideas": interpolation,
        "Section_Length_Notes": songmath,
        "Streaming_Optimizer_Feedback": streaming,
        "Viral_Maximizer_Feedback": viral,
        "Hook_Impact_Feedback": hooktest,
        "Arrangement_Feedback": arrangement,
        "Key_BPM_Suggestion": keybpm
    }
