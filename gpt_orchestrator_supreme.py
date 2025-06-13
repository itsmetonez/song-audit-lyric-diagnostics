from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import logging

# Initialize app
app = FastAPI()

# Enable logging for debugging
logging.basicConfig(level=logging.DEBUG)

# Define incoming request schema
class SupremeRequest(BaseModel):
    lyrics: str
    reference_song: Optional[str] = None
    target_emotion: Optional[str] = None
    optimize_rap_punchlines: Optional[bool] = False
    optimize_hood_bars: Optional[bool] = False
    target_genre: Optional[str] = None

# Health check route (optional)
@app.get("/")
def root():
    return {"message": "Supreme Orchestrator is online!"}

# Main orchestrator route
@app.post("/gpt_orchestrate_supreme")
async def gpt_orchestrate_supreme(request: SupremeRequest):
    # Log full payload for debugging
    logging.debug(request.dict())

    # Dummy processing for now
    # This is where we will add all the Supreme hitmaker logic next
    
    result = {
        "lyrics": request.lyrics,
        "reference_song": request.reference_song,
        "target_emotion": request.target_emotion,
        "punchline_opt": request.optimize_rap_punchlines,
        "hood_opt": request.optimize_hood_bars,
        "genre": request.target_genre,
        "status": "✅ Orchestration processed successfully (stub mode)"
    }

    return result

