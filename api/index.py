# file: api/index.py (FINAL, COMPLETE VERSION)

from fastapi import FastAPI, Depends, HTTPException, status
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

# --- Lobby Endpoint (for GET pings) ---
@app.get("/")
async def get_root():
    return {"status": "Isabella Agent is online and ready."}

# --- NEW: Reception Desk / Discovery Endpoint ---
# This responds to the Agent Builder's POST request to discover tools.
@app.post("/")
async def discover_tools():
    """
    Returns an OpenAPI schema describing the available tools.
    This allows the Agent Builder to "load the tools".
    """
    schema = {
        "openapi": "3.1.0",
        "info": {"title": "Isabella Scraper Tools", "version": "1.0"},
        "paths": {
            "/api/invoke": {
                "post": {
                    "summary": "Invoke Isabella Scraper",
                    "description": "Takes a URL, scrapes it, and enhances the content using the Isabella brand voice.",
                    "operationId": "invoke_isabella_agent",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "url": {
                                            "type": "string",
                                            "description": "The URL of the webpage to process."
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {"200": {"description": "Successful Response"}}
                }
            }
        }
    }
    return schema
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
    enhanced_text = enhance_with_isabella_voice(raw_text)
    if enhanced_text.startswith("Error:"):
        return {"error": enhanced_text}
    return {"enhanced_content": enhanced_text}
