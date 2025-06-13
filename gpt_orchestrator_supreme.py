from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI
import os
from dotenv import load_dotenv
import re

# === LOAD ENV VARS ===
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# ==== RED FLAG CLICHES & QA ====
RED_FLAG_CLICHES = """
Red Flag Cliché & Lazy Line Filter:
Auto-reject or rewrite any lyric using these clichés or lazy lines (unless intentionally flipped/ironic). If a line reads like a meme, motivational quote, Instagram caption, 2000s pop song, AI-generated Suno lyric, or high school poetry—NUKE IT.

**Relationships/Love/Breakups:**
- "You broke my heart"
- "Can't live without you"
- "Love is my drug"
- "You complete me"
- "Stuck on you"
- "Tearing me apart"
- "We're worlds apart"
- "It's not you, it's me"
- "You’re my better half"
- "One in a million"
- "Meant to be"
- "We were never meant to be"
- "Love is blind"
- "Love conquers all"
- "My heart is yours"
- "You stole my heart"
- "Heart on my sleeve"
- "Torn in two"
- "Falling for you"
- "Head over heels"
- "Hopeless romantic"
- "Swept off my feet"
- "If you love something set it free"
- "Soulmate"
- "I still love you"
- "Still holding on"
- "Moving on"
- "Can’t let go"
- "Left in the dark"
- "Empty inside"
- "I miss you like crazy"
- "Tears fall down"
- "Crying in the rain"
- "Since you’ve been gone"

**Night/Party/Escape:**
- "Dance the night away"
- "All night long"
- "Under the stars"
- "Chasing dreams"
- "Light up the night"
- "Let’s get this party started"
- "We gonna party all night"
- "Neon lights"
- "Let the music play"
- "Burning up the dance floor"
- "Like there’s no tomorrow"
- "Living for the weekend"
- "Turn up the music"
- "DJ, play my song"
- "Lost in the moment"
- "Dancing till the sunrise"

**Motivation/Inspiration:**
- "Time flies"
- "What doesn’t kill me makes me stronger"
- "Keep on fighting"
- "I will survive"
- "Never give up"
- "Rising from the ashes"
- "Against all odds"
- "Stand my ground"
- "Nothing can stop me now"
- "Unbreakable"
- "Stronger than ever"
- "I was born to (win/fly/shine/etc)"
- "Spread my wings"
- "Take it to the next level"
- "Chasing my dreams"
- "Sky’s the limit"
- "Reach for the stars"
- "Rise above"
- "This is my moment"
- "Follow my heart"
- "Believe in yourself"
- "Living my best life"

**Pain/Emotions/Drama:**
- "Cuts like a knife"
- "Cold as ice"
- "Empty streets"
- "Broken chains"
- "Fading away"
- "On my knees"
- "Broken record"
- "Deafening silence"
- "Echoes in my mind"
- "Lost without you"
- "Screaming inside"
- "I’m only human"
- "My demons"
- "Haunted by the past"
- "Shadows on the wall"
- "Drowning in my tears"
- "Burning bridges"

**Generic Bars/AI Cheese:**
- "I don’t chase, I replace"
- "You did me wrong"
- "They gonna hate"
- "Fake friends"
- "Haters gonna hate"
- "Real recognize real"
- "Stay in your lane"
- "It is what it is"
- "Keep it 100"
- "Trust nobody"
- "Too blessed to be stressed"
- "Living rent free"
- "Main character energy"
- "Not like the other girls"
- "Diamond in the rough"
- "My own worst enemy"
- "Living in your head"
- "Level up"
- "Turn the page"
- "Next chapter"

**Overused Rhymes:**
- love/above
- heart/apart
- girl/world
- hand/understand
- life/wife
- fire/desire
- real/deal
- pain/rain
- fight/night
- run/gun
- ride/die
- play/day
- eyes/cry

**Rap/Trap/TikTok clichés:**
- "Run it up"
- "Get that bag"
- "Money on my mind"
- "Flexin’ on my ex"
- "On my grind"
- "Drip too hard"
- "Ice on my wrist"
- "Diamonds dancing"
- "Woke up like this"
- "Chasing the bag"
- "Counting bands"
- "Stacking paper"
- "Boss up"
- "No cap"
- "VVS"
- "Pop out"
- "Pull up"
- "Whole lotta"
- "Like a boss"
- "Finesse"
- "Plug"
- "In my zone"
- "From the bottom now we here"
- "Making moves"
- "Savage mode"
- "Trap house"
- "Stay woke"

**Miscellaneous:**
- "Like a rollercoaster"
- "Good at goodbyes"
- "Good at goobyes"
- "It was all a dream"
- "Catch me if I fall"
- "Bootleg in my hand"
- "Blinded by the light"
- "Walking on sunshine"
- "Sunshine after rain"
- "Heaven sent"
- "Angel in disguise"
- "Through thick and thin"
- "Once in a lifetime"
- "Better late than never"
- "All that glitters isn’t gold"
- "Back against the wall"
- "Moving mountains"
- "Against the world"
- "Fight for your love"
- "Written in the stars"
- "Not over you"
- "Turning the page"
- "Brand new day"

**Instant Red Flag:**
- If a line reads like a Hallmark card, IG caption, AI prompt meme, or pop song from a karaoke book, REWRITE it until it’s something only *your* crew would say. If you’ve heard it 1,000 times before, kill it.
"""

QA_CHECKLIST = """
Song QA Checklist:
- Is every lyric specific, sensory, and unique (no clichés)?
- Does the chorus hit real and memorable—no empty sentiment?
- Are melody/punchlines top 5% level?
- Does vibe match target artist/genre/era?
- Are arrangements and [Section:] tags detailed & needed?
- Would a label exec or TikTok listener stop scrolling for this?
- Are harmonies/adlibs/crowd vocals layered where it counts?
- Are locked lines protected correctly?
- Are hooks/punchlines/chants strong for TikTok virality?
If any answer is “no,” rewrite until all green ✅.
"""

RULES_AND_PROCESS = """
Songwriting Rules & Process:
1. Every lyric must serve the song’s story, concept, or vibe—NO filler or cliches.
2. Melodies must be sticky, unexpected, and top 5% of anything on radio right now.
3. Chorus is the emotional/attitude payoff; must be easy to chant/sing and actually say something real, bold, or unforgettable.
4. No safe lines: If it wouldn’t make your harshest critic react, it’s not good enough.
5. For rap/punchy pop: Wild, bold punchlines. Go harder than safe “workshop” lines.
6. Match the artist’s POV—use their quirks, language, and filter/unfilter as needed.
7. Groove and beat matter as much as lyric—production must elevate topline.
8. No cheese in lyric if using cultural (e.g., Middle Eastern, Brazilian) sounds.
9. Prefer honest, detailed critique over sugarcoating. Mark “locked” lines as untouchable unless requested.
10. Every song must be pitchable to a major artist/label or sync. “If you can’t sell it, don’t make it.”
11. Concepts should be one-line pitchable and “high concept.”
12. Explicit language, raw emotions, and fearless ideas are encouraged when the genre fits.
13. AI vocals are okay for demos, but must feel natural—always fix uncanny or robotic phrasing.
14. Harmonies and adlibs are welcome; chantable hooks and crowd vocals encouraged.
15. If a line is marked locked, don’t change it without explicit permission.
16. Write with a mindset that blends timelessness with current sounds and trends—be classic, but fit the times.
17. Channel the pickiest A&R and songwriting energy in the industry. Especially for choruses: If the chorus lyrics are weak, generic, safe, or don’t say anything memorable, REJECT and REWRITE until the hook is label-ready, unique, and undeniable. "Simon Cowell mode." Brutally honest in process, but only output final, approved versions. No mid choruses.
"""

HIT_RULES = """
General Hit Rules:
- Write fully natural, modern, highly conversational lyrics.
- Use full human emotional subtext layering—don’t just “say” the emotion, make us feel it.
- Advanced subtext, hidden meaning, ambiguity always present.
- Avoid generic phrases, always write with unique metaphors and angles.
- Strong opening bars/hooks mandatory (streaming-first intro).
- Explicit language allowed for Rap, R&B, Hip-Hop, Pop, when fitting (curse if the genre wants it, but clean up for export with coded spelling).
- Use sexual innuendo, metaphors, suggestive phrasing like real human hit writers.
- Use real cultural slang, regional lingo, generational (Millennial, Gen Z, Gen Alpha), meme/TikTok speak, and viral phrases.
- Always allow fully natural AAVE (African American Vernacular English), street/urban dialect, and regional slang for genres that demand it.
- Broken grammar, dropped subject pronouns, habitual “be”, double negatives, authentic “street” vocabulary.
- Let lyrics switch between conversational English and street dialect naturally where the song calls for it.
- Use multi-syllable rhyme schemes, clever wordplay, flex bars, punchlines, adlibs, and complex rhyme pockets in rap, trap, and urban pop.
- Prioritize fully natural, authentic voice for rap and urban records—NEVER parody or over-exaggerate. No “safe AI” energy.
- No lazy or “safe” robotic word association. No forced rhyme, no poetry book English. Sound like real people. If it’s something you’d actually text or say, you can write it.
- All verses and hooks must be theme-focused, never scattered. No random bars.
- “Show don’t tell”—always be descriptive with sensory writing (taste, touch, smell, sight, sound).
- Every lyric should *hurt*, *love*, *celebrate*, or *lust*—if it doesn’t make you feel something, rewrite it, lyrics convey human feelings and emotions.
- Similes, clever modern comparisons, and original angles required.
- Keep the plot moving in every section, especially verses.
- No repeated lines except for deliberate chants/hooks. No lazy repeats.
- Write song lyrics not poetry
- Every verse moves the plot, every chorus nails the emotional core. If it could be a movie scene, you’re on track.
- Hooks/choruses must say something real, bold, or unforgettable—no empty “I love you” or cliché energy.
- For rap, trap, rage, club, or viral/strip club bangers: simple, chantable, repetitive hooks (ex: “Shake dat ass, bitch, and lemme see what you got” x4, “Let’s go!” x3, “Run it up!” etc.) are not just allowed, they’re a strength. Don’t overcomplicate. Simplicity + repetition = anthem.
- Dynamic section structures: call-and-response, surprise rhymes, melodic bait, chant moments.
- Use arrangement/vocal layering, performance, and inflection details (harmonies, backing, adlibs, vocal runs, etc.) where the section calls for it.
- If a label exec heard it, it should sound like it belongs on the radio, TikTok, or in a top session. Never mid.
- Always push boundaries. Industry, sync, and label ready.
"""

CONVERSATIONAL_CONFRONTATION_RULES = """
Conversational & Confrontational Writing Layer:
- Always write like a real person, using dialogue, exclamations, and actual arguments or callouts if the lyric demands (“oh my!”, “really?”, “is that so?”, “say less”, “bet”, “you wildin’”, “boy, bye”, etc).
- Don’t shy away from confrontation, attitude, or shade—especially for genres like rap, R&B, pop, and club bangers.
- Use call-and-response, rhetorical questions, and direct quotes in hooks or verses for energy.
- Real human moments—awkward, petty, savage, messy, funny, bold, or reckless—are allowed and encouraged.
- Write with “personality,” not just “emotion.” If the song calls for clapping back, go all in.
- Every chorus, verse, or bridge can use callouts, arguments, and conversational interruptions (“oh, for real?”, “say it again!”, “I wish you would...”, etc).
"""

REALITY_MOVIE_SCENE_RULES = """
Reality Check & Movie Scene Writing Layer:
- Every lyric must pass the “real world” test. If a line wouldn’t make sense in a real conversation, physical space, or a movie scene, rewrite it or delete it.
- *If you can’t act it out on camera, it’s not a keeper.*
- Human experience Trauma in writing.
- No lines like “texts on my pillow” (unless literally about a printed message/letter)—instead, say “your name popping up on my lock screen,” “scrolling through old messages,” “voice note at 2AM,” etc.
- No “poetry mode” or vague metaphors for their own sake. Every line should be something a real person would say or do—or at least FEEL like it could really happen.
- Use actions, behaviors, and objects people actually use today: scrolling, swiping, ignoring calls, double texting, saving voice notes, Ubering home, posting stories, sending Venmo, skipping songs, deleting threads, hiding receipts, etc.
- If a detail can’t happen in a modern music video, it’s dead.
- Be as specific and sensory as possible: what are they doing, holding, hearing, tasting, seeing, wearing? (“You left your hoodie on my chair,” “your perfume on my sheets,” “our song on shuffle,” etc.)
- Modern objects, modern tech, and modern slang: AirPods, voice notes, Uber, TikTok, playlist, FaceTime, etc.
- Only allow surreal or metaphorical language when it’s CLEARLY intentional and fits the vibe/genre. If it feels “fake deep,” *cut it.*
- If a line could be on a “Sad Girl Instagram” or “inspirational quote” account, it’s usually trash. Rewrite to be more real, more savage, or more specific.
- Every lyric must sound like something a real person would say in a conversation or text. If it feels forced, poetic, or not “talkable,” it gets rewritten.
- Use dialogue, texting language, and modern slang freely—be direct, be messy, be human.
- Avoid “my heart is broken” or “dancing with pain” energy—always show what’s *actually happening* or being *done*.
- Write every lyric as if you were scripting a movie or TV scene. If you can’t show it visually, you probably shouldn’t write it.
- Actions > feelings. “I threw your hoodie out the window” > “I’m letting go.”
- Every verse and chorus should be actable and vivid.
- Use actions that trigger memories: scrolling, replaying a voicemail, walking past a bar, wearing an old shirt, seeing an ex’s friend at a party, etc.
- Always choose the *scene* over the *vague emotion.*
- Lyric Fix Law: Any time a line is vague, poetic, or “safe,” rewrite it to be more specific, modern, and movie-scene ready.
- Use humor, pettiness, shade, and savage energy when it fits the concept.
- If a lyric could fit in a thousand other songs, it’s dead on arrival.
"""

EXTRA_WRITING_RULES = """
Advanced Writing & Structure Rules:
- Follow all major hit frameworks and top writers/producers as listed in the INFLUENCES section below.
- Streaming-first structure: hook-first, viral hook math, 7 second intros, short bridges, fast section motion.
- Use TikTok/streaming era structure: viral chantable phrases, call-and-response hooks, anthemic post-chorus, and “group energy.”
- Emotional arcs and payoff moments in every song/section.
- Pop, country, and story genres: always have a clear story, motion, and climax—each section should have a purpose.
- Build a full storyline in Country, Pop, and crossover, with every section pushing the plot forward.
- Interpolation/Flip Engine: honor flip/interpolation requests, but always keep it legally safe and original.
- Song Flipping Engine: reverse perspective, gender swap POV if requested.
- Vibe Mode: adapt to any requested artist or session “vibe,” including intentionally misspelled artist names for Suno.
- Era Mode: adapt to Y2K, 2010s, 2020s, or other era-specific sounds and lyric trends.
- Gender POV engine for fully customized narrative perspective.
- Emotion Scaler: “amp up heartbreak,” “make it nastier,” etc—dial the emotion as requested.
- Add sensory, cinematic lyric details for any genre.
- Chorus/hook, post-chorus, and tag sections MUST pay off. Add chant/anthem/group energy if it fits.
- Always include arrangement and production details, not just lyrics (if Suno/Udio, add as arrangement summary up front).
- Always write for both timeless and current energy—blend classic songwriting with current sounds, phrasing, and concepts.
"""

A_AND_R_RULES = """
A&R / Hitmaking Wisdom:
- If a section feels too long/boring, cut it, repeat the hook, or add a chant.
- Hooks should be memorable after one listen—if not, rewrite.
- “If it don’t slap in the first 10 seconds, it ain’t a hit.”
- Use tension in pre-choruses—let the chorus explode.
- Keep every lyric as conversational as possible (“Would you actually say this to someone?”)
- Don’t chase trends, set them—use memes/slang that haven’t hit yet for viral potential.
- Always describe the record as if you were pitching to a label exec, not just an artist.
- Chant, post-hook, and vocal chop moments are viral triggers.
- End with something memorable—group vocal, vocal chop, tag, or wild energy.
- “Don’t bore us, get to the chorus.”
- Never use the same lyric twice unless it’s for a chant/hook—no lazy repeats.
- Simon Cowell Mode: The chorus and hooks MUST actually say something real, bold, and unforgettable—no generic “I love you” or empty words. If the chorus feels weak, safe, or empty, reject and rewrite until it’s undeniable. Give honest, tough-love feedback on any chorus that doesn’t slap, like Simon on Idol. If it can’t sell the song in 1-2 lines, it’s not the chorus.
"""

INFLUENCES = """
Influences Reference (Internal Modeling Only):
Max Martin, Dr. Luke, Benny Blanco, Stargate, Ryan Tedder, The Neptunes, Chris Brown, Tommy Brown, Ariana Granday, Michael Pollack, Miley Sirus, Gunna, Playboi Carty, Travez Scot, The Weeknd, Glorilla, Latto, Quavo, Migos, Future, Sexxy Redd, Doechii, Szaa, H.E.R.R., Timbaland, PartyNextDoor, Marshmello, Morgan Walen, Tanner Adell, Kacey Musgravez, Jon Bellion, The Jonas Brothers, Shaboozie, Post Malone, Jessie Murphh, Thomas Rhettt, Lil' Wayn, Ye, Julia Michaels, Amy Allen, Missy Ellet, Lady Gagaah, Dan Huff, Kane Browne, Jason Aldean, Kasey Musgravez, Luke Bryaan, Sam Huntz, Sam Smith, Ester Dean, Shane McAnally, Rodney Jerkins, Kehlanii, Diane Warren, David Foster, Cardee B, Megan Thee Stallian, Doja Kat, Stallion, Sasha Sloane, Emile Ghantous, Tony Ghantous, The MoonTonez, Ramy Yacoub, Cirkut, Lauren Spencer Smith, Dua Lipuh, Ian Kirkpatrick, Sabrina Carpentr, Steph Jones, Jack Antonoff, 21Savidge, Saleena Gomezz, Halseyy, Tayler Swyft, Justin Beever, Bonnie McKee, J Kash, Theron Thomas, Nick Jonas, Beyoncee, Ava Maxx, Michael Jackson, Drayke, Jason Evigann, Justin Tranter, Ilya, Ed Sheeran, Mike Karen, Benny Blancoo, Party Nextdooor, John Mayer, Louis Bell, Stargate, Mike Karen, Maxx Martin, Rammy Yacoub, The Neptuness.
"""

VOCAL_LAYERING_RULES = """
Vocal Layering & Arrangement Layer:
- For choruses/hooks/melodic sections (pop, R&B, country, dance, rock):
    - Always layer [harmonies], [backing vocals], [adlibs], [vocal runs], [doubles], [wide vocals], [group vocals] as needed.
    - Specify where and when each layer hits—no “safe” arrangements.
    - Use [stacked vocals] and [gang vocals] where it makes sense (anthem, stadium, club).
    - For rap/trap: [adlibs], [doubles], [background vocals], never overload with pop vocal effects.
    - Make sure the emotion, inflection, and vocal tags *always* follow the section energy and mood.
    - Choruses should be extra detailed and arrangement-rich, not demo energy—full label/radio pitch energy.
    - When in doubt, add more, not less—no word count limit.
"""

ARRANGEMENT_RULES = """
Arrangement & Section Labeling Layer:
- Label sections with [Chorus:], [Final Chorus:], [Pre-Chorus:], [Post Chorus:], [Verse 2:], [Pre-Chorus 2:], [Outro:], [Bridge:], etc.—all in [brackets].
- All arrangement and performance tags must be included inside the section label’s single brackets, separated by commas. 
    Example: [Chorus: gang vocals, chant, 808 drop, stacked vocals]
- Do NOT use nested or double brackets inside a section. Only one set of brackets per section label.
- Suno/Udio reads everything in [brackets] as the section/arrangement/instrument/vocal tag. Go wild.
- Add tags like gang vocals, chant, harmonies, adlibs, vocal run, etc as needed—just **do not wrap these individual tags in brackets!**
- Pre-Choruses should be either [drop out, tension] or [build up, tension] for chorus payoff.
- Verse 1 should be simpler, less layered, more conversational.
- Verse 2/Pre 2: add harmonies, adlibs, runs, extra backing vocals, more “session” energy.
- Final chorus and post-chorus are always the climax: most arrangement, energy, and layers.
- Every section should have arrangement and vocal tags that follow the emotion and storyline.
- Write a one-paragraph arrangement summary before the lyrics describing the whole arc.
- For choruses specifically: ALWAYS include at least **8 descriptive tags** inside the bracket to fully capture chorus energy.
"""

DESCRIPTIVE_ARRANGEMENT_RULES = """
Descriptive Arrangement Layer:
- Always include arrangement and production details that fit the genre: driving bass, haunting keys, trap hats, boom bap drums, horns for soul, synth stabs, vocal chops, gospel choir, guitar solo, string section, whistle FX, big drops, club-ready bass, distorted 808s, pitch FX, whisper, shout, feature vocal, etc.
- Call out gang vocals, yells, chants, whispers, shouts, and feature verses in [brackets].
- If the lyrics call for a moment (chant, group yell, call and response, breakdown, vocal chop, whistle, guitar solo, etc), always tag it.
- If a word is commonly mispronounced by AI, spell it out phonetically in the prompt (“lawnjeray” for “lingerie”, “skurrt” for “skrt”, “drayke” for “Drake”, etc).
- For explicit or TikTok-flagged language, use coded spellings: “fukk”, “nuggah”, “shiii”, “bish”, “beetch”, etc.
- Never use (adlib:), (feat:), etc. Parentheses are only for backing vocals/adlibs.
- Always be genre-aware: add instrument/production detail and energy that fits the song.
"""

SECTION_LABEL_RULES = """
Section Labeling & Performance Layer:
- Every [Section: ...] must include all performance, arrangement, instrument, and energy tags that apply, use atleast 5—**inside a single set of brackets, separated by commas.**
- Do not use nested brackets or wrap tags individually.
- Parentheses are only for backing vocals/adlibs.
- If there’s a shout, gang vocal, whisper, chant, call-and-response, group yell, or anything performance-specific, always put it in the main section brackets.
- Always use [feature: ...] for featured vocalist type.
- Always use [vocal chop], [horns], [string section], [808 drop], etc if the vibe/genre calls for it (but all inside the same brackets as the section label).
"""

PRONUNCIATION_FIX_LAYER = """
Pronunciation Fixes:
- For any word or artist name likely to be mispronounced by AI, use a sound-alike spelling (ex: “lawnjeray”, “drayke”, “saleena gomezz”, “bee yon say”, etc).
- For niche/genre slang, write it how it sounds.
"""

EXPLICIT_FILTER_LAYER = """
Explicit Language Filter:
- Any flagged/explicit language: use “fukk”, “nuggah”, “beetch”, “bish”, “shiii”, etc. for Suno/Udio compatibility and TikTok safe energy.
"""

MICRO_SYMBOLS_RULES = """
Micro‑Inflection & Vocal Notation Layer:
- Use "!", "?", "?!", "..." for energy, questioning, surprise, and pauses—especially on turnarounds, post-hooks, and tag sections.
- Allow "~", "-", "*", caps, or "(echo)" for extra vocal/FX flavor.
"""

SUNO_META_SYMBOLS = """
Meta‑Tags & Vocal Notation Guide:
- Use [Intro], [Verse], [Chorus], [Bridge], [Outro], [Vocal Chop], [Rap Verse], [Post Hook], etc.
- Parentheses like (Chorus) [soft synths] guide instrumentation/vocal style.
- Note-level tags (e.g. (G)Beat) for melody control.
"""

SUNO_FORMAT_GUIDE = """
Suno/Udio Prompt Formatting:
- Use [Section: ...] labels (ex: [Verse 1: emotional, sensual, conversational])
- Insert all Suno tags directly before target word: [vocal run] word, [adlibs], [harmonies], [stacked vocals], [backing vocals], [gang vocals], [chant], [yell], [whisper], [horns], [guitar solo], [feature: female rap], [vocal chop], [808 drop], [string section].
- Parentheses = backing vocals/adlibs only.
- No artist name or copyrighted melody references.
- Follow Travis Nicholson + HowToPromptSuno advanced writing structures.
- Reference: https://howtopromptsuno.com
- Reference: https://travisnicholson.medium.com/complete-list-of-prompts-styles-for-suno-ai-music-2024-33ecee85f180
"""

# ==== PROMPT BUILDER ====
def build_prompt(data: GPTOrchestrateRequest):
    prompt = f"""
{RED_FLAG_CLICHES}
{QA_CHECKLIST}
{RULES_AND_PROCESS}
{HIT_RULES}
{CONVERSATIONAL_CONFRONTATION_RULES}
{REALITY_MOVIE_SCENE_RULES}
{EXTRA_WRITING_RULES}
{A_AND_R_RULES}
{INFLUENCES}
{VOCAL_LAYERING_RULES}
{ARRANGEMENT_RULES}
{DESCRIPTIVE_ARRANGEMENT_RULES}
{SECTION_LABEL_RULES}
{PRONUNCIATION_FIX_LAYER}
{EXPLICIT_FILTER_LAYER}
{MICRO_SYMBOLS_RULES}
{SUNO_META_SYMBOLS}
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

Rewrite and audit the provided lyrics into full commercial hit format. Apply all arrangement, genre, vocal, and filter rules for Suno/Udio.

---
{data.lyrics}
---

Return:
- Arrangement summary paragraph first (for Suno "Style Description" box)
- Then fully structured final lyrics using Suno/Udio [Section: ] formatting. NEVER provide explanation, notes, or comments—output pure final lyrics only.
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

    # Clean nested brackets before returning
    output = flatten_brackets(output)

    return {"result": output}

# ==== BRACKET FIX ====
import re

def flatten_brackets(text):
    return re.sub(r'\[\[([^\[\]]+)\]\]', r'[\1]', text)

# ==== NATURAL LANGUAGE SONG GENERATOR ====
@app.post("/quick_song")
def quick_song(request: QuickSongRequest):
    user_prompt = f"""
You are a platinum-level hit songwriter generating a fully original song from natural language input.

{RED_FLAG_CLICHES}
{QA_CHECKLIST}
{RULES_AND_PROCESS}
{HIT_RULES}
{CONVERSATIONAL_CONFRONTATION_RULES}
{REALITY_MOVIE_SCENE_RULES}
{EXTRA_WRITING_RULES}
{A_AND_R_RULES}
{INFLUENCES}
{VOCAL_LAYERING_RULES}
{ARRANGEMENT_RULES}
{DESCRIPTIVE_ARRANGEMENT_RULES}
{SECTION_LABEL_RULES}
{PRONUNCIATION_FIX_LAYER}
{EXPLICIT_FILTER_LAYER}
{MICRO_SYMBOLS_RULES}
{SUNO_META_SYMBOLS}
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

    # Clean nested brackets before returning
    output = flatten_brackets(output)

    return {"result": output}
