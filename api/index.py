# file: api/index.py (DEBUGGING VERSION)

from fastapi import FastAPI, Request
from pydantic import BaseModel

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/api/invoke")
async def invoke_isabella_agent(request: Request, body: ScrapeRequest):
    """
    This is a temporary endpoint to debug incoming requests.
    It will log the headers and body it receives.
    """
    
    # --- THIS IS THE DETECTIVE CODE ---
    print("--- NEW INCOMING REQUEST ---")
    print("Headers:")
    # Print all the headers that the Agent Builder is sending
    for name, value in request.headers.items():
        print(f"  {name}: {value}")
    
    print("\nBody:")
    # Print the body that the Agent Builder is sending
    print(f"  {body.dict()}")
    print("--------------------------")
    # --- END DETECTIVE CODE ---

    # We will just return a simple success message for now
    return {"status": "Request received and logged successfully."}
        
    print("--- Enhancement successful. Returning result. ---")
    
    # Return the final, beautifully written text
    return {"enhanced_content": enhanced_text}
