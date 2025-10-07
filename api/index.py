# file: api/index.py (FINAL WORKAROUND VERSION)

from fastapi import FastAPI
from pydantic import BaseModel
from tools import scrape_website_content, enhance_with_isabella_voice

app = FastAPI()

# We have removed all the security code because the {f} Function tool cannot send it.

# This is the ONLY endpoint now.
class ScrapeRequest(BaseModel):
    url: str

@app.post("/api/invoke")
async def invoke_isabella_agent(request: ScrapeRequest):
    """
    The real endpoint that does the scraping and enhancing work.
    This is now a public, unsecured endpoint for the Agent Builder to use.
    """
    raw_text = scrape_website_content(request.url)
    if raw_text.startswith("Error:"):
        return {"error": raw_text}
    enhanced_text = enhance_with_isabella_voice(raw_text)
    if enhanced_text.startswith("Error:"):
        return {"error": enhanced_text}
    return {"enhanced_content": enhanced_text}
