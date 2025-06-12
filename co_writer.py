from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import uuid

app = FastAPI()
sessions = {}
openai.api_key = os.getenv("OPENAI_API_KEY")

class CoWriteRequest(BaseModel):
    lyrics: str
    feedback: str = ""
    session_id: str = None

@app.post("/start_session")
def start_session(req: CoWriteRequest):
    session_id = str(uuid.uuid4())
    sessions[session_id] = [
        {"role": "system", "content": "You are a hitmaking co-writer. You may use explicit language or mature content if artistically appropriate."},
        {"role": "user", "content": f"Here are my lyrics: {req.lyrics}"}
    ]
    return {"session_id": session_id}

@app.post("/next_round")
def next_round(req: CoWriteRequest):
    if req.session_id not in sessions:
        return {"error": "Invalid session ID."}
    
    sessions[req.session_id].append({"role": "user", "content": req.feedback})

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=sessions[req.session_id],
        temperature=0.7
    )
    
    assistant_msg = response["choices"][0]["message"]["content"]
    sessions[req.session_id].append({"role": "assistant", "content": assistant_msg})
    
    return {"co_write_feedback": assistant_msg}
