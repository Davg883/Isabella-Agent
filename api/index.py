# file: api/index.py

from fastapi import FastAPI
from pydantic import BaseModel
# Import the two "superpower" functions we just created
from tools import scrape_website_content, enhance_with_isabella_voice

app = FastAPI()

# Define the input format for our API. It just needs a URL.
class ScrapeRequest(BaseModel):
    url: str

@app.post("/api/invoke")
async def invoke_isabella_agent(request: ScrapeRequest):
    """
    This endpoint receives a URL, scrapes it, enhances the content, and returns the result.
    """
    print(f"--- Received request to process URL: {request.url} ---")
    
    # Step 1: Scrape the website
    raw_text = scrape_website_content(request.url)
    if raw_text.startswith("Error:"):
        return {"error": raw_text}

    print("--- Scraping successful. Enhancing text... ---")

    # Step 2: Enhance the scraped text
    enhanced_text = enhance_with_isabella_voice(raw_text)
    if enhanced_text.startswith("Error:"):
        return {"error": enhanced_text}
        
    print("--- Enhancement successful. Returning result. ---")
    
    # Return the final, beautifully written text
    return {"enhanced_content": enhanced_text}