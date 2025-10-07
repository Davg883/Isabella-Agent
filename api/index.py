# file: api/index.py (FINAL VERSION)

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os
from tools import scrape_website_content, enhance_with_isabella_voice

app = FastAPI()

# --- Security Setup ---
security_scheme = HTTPBearer()
SECRET_TOKEN = os.getenv("BEARER_TOKEN") 

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    if not SECRET_TOKEN or credentials.scheme != "Bearer" or credentials.credentials != SECRET_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
        )

# --- NEW: Add a 'Lobby' Endpoint ---
# This is the front door that the Agent Builder will ping.
@app.get("/")
async def get_root():
    """A simple endpoint to confirm the server is running."""
    return {"status": "Isabella Agent is online and ready."}
# --- END NEW ---


# --- The Original, Real Tool Endpoint ---
class ScrapeRequest(BaseModel):
    url: str

@app.post("/api/invoke", dependencies=[Depends(verify_token)])
async def invoke_isabella_agent(request: ScrapeRequest):
    """The real endpoint that does the scraping and enhancing work."""
    raw_text = scrape_website_content(request.url)
    if raw_text.startswith("Error:"):
        return {"error": raw_text}
    enhanced_text = enhance_with_isabella_voice(raw_text)
    if enhanced_text.startswith("Error:"):
        return {"error": enhanced_text}
    return {"enhanced_content": enhanced_text}
