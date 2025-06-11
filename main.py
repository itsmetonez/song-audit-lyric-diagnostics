from fastapi import FastAPI
from pydantic import BaseModel
from collections import Counter

app = FastAPI()

class LyricsRequest(BaseModel):
    lyrics: str

@app.post("/analyze")
def analyze_lyrics(request: LyricsRequest):
    lyrics = request.lyrics.lower()

    # ULTRA EXPANDED CLICHÉ LIST
    cliche_list = [
        "chasing shadows", "heart on fire", "lost control", "in my head", "i don’t chase i replace",
        "broken pieces", "demons inside", "rise from the ashes", "falling for you", "fading away",
        "my broken heart", "tears falling down", "darkness inside", "lost without you",
        "burning desire", "haunted by you", "you’re my everything", "soul on fire", "take me higher",
        "drowning in your love", "i can't breathe without you", "lost in the moment",
        "you complete me", "i'm nothing without you", "unbreak my heart", "head over heels",
        "writing on the wall", "walking on thin ice", "empty inside", "living a lie",
        "you're my angel", "wings to fly", "fire and ice", "time stands still",
        "eternally yours", "waiting for you", "under your spell", "holding on",
        "dreams come true", "stars align", "perfect storm", "burning bridges",
        "crossroads ahead", "battle within", "piece of my heart", "lost and found",
        "deep down", "one in a million", "once in a lifetime", "shattered dreams",
        "my destiny", "forever and always", "written in the stars", "without a trace",
        "bleeding heart", "never let go", "i surrender", "broken promises", "lost my way",
        "missing piece", "one more night", "broken inside", "love of my life", "nightmare ending",
        "stormy weather", "lonely road", "fight for love", "unspoken words", "healing wounds",
        "wasted time", "i was blind", "wasted love", "run away from love", "game of love",
        "love is war", "battle scars", "never enough", "searching for you", "fool for you",
        "cold as ice", "burn like fire", "lost cause", "endless nights", "forever lost",
        "frozen heart", "light in the dark", "heaven and hell", "take me home", "ride or die",
        "rollercoaster ride", "toxic love", "built to break", "haunted memories",
        "walls closing in", "out of control", "second chance", "torn apart", "lost forever",
        "i'm him", "i'm her", "i'm not the one", "i'm the prize", "she’s a 10 but", 
        "he fumbled the bag", "you lost me", "it's giving", "stay toxic", 
        "i upgraded", "level up", "bossed up", "i’m built different", 
        "silent moves", "move in silence", "i eat alone", "no new friends",
        "i'm on demon time", "matching energy", "energy shift", "protecting my peace",
        "unbothered", "left on read", "ghosted", "glowed up", 
        "can't compete where you don't compare", "you broke me", "i gave you my all", "trust issues", 
        "it's complicated", "we were meant to be", "couldn't love me right", "late night texts",
        "losing sleep over you", "haunted by your memory", "can't live without you",
        "cold heart", "you're my weakness", "my heart can’t take this", "pain runs deep",
        "main character energy", "that part", "say less", 
        "mood swings", "red flags", "soft launch", "situationship", 
        "the audacity", "low key", "high key", "it’s giving toxic",
        "it’s giving single", "my villain origin story", "outside but dead inside",
        "love is blind", "bulletproof heart", "king and queen", 
        "i'm falling apart", "never good enough", "holding me back",
        "the one that got away", "meant to be", "forever yours",
        "nothing lasts forever", "if you only knew", "i'll never love again",
        "can't lose you", "wasted love"
    ]

    # ULTRA EXPANDED FILLER WORDS LIST
    filler_words = [
        "just", "really", "kinda", "sorta", "baby", "like", "maybe", "gonna", "wanna", "i think",
        "gotta", "you know", "forever and always", "never ever", "always", "someday", "honestly",
        "truthfully", "so much", "literally", "basically", "obviously", "lowkey", "highkey",
        "deep down", "after all", "without a doubt", "no matter what", "for real", "by my side",
        "right now", "somehow", "in my head", "in my heart", "for you", "i swear", "baby girl",
        "truly", "really love", "tryna", "sorta kinda", "super", "all the way",
        "still", "even", "still got", "so many", "always been", "kinda like", "always thought",
        "i mean", "i guess", "actually", "especially", "somewhere", "something", "nothing much",
        "anything", "everything", "somebody", "anyone", "no one", "everyone"
    ]

    # ULTRA EXPANDED PREDICTABLE RHYMES LIST
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

    # SCANNERS
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
