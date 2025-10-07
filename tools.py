# file: tools.py

import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os

# Initialize the OpenAI client. It will use the OPENAI_API_KEY from your environment variables.
client = OpenAI()

def scrape_website_content(url: str) -> str:
    """Fetches and extracts the main text content from a given URL."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # A simple scraper to get all text. More advanced versions could target specific tags.
        main_content = soup.body.get_text(separator='\\n', strip=True)
        return main_content
    except requests.exceptions.RequestException as e:
        return f"Error: Could not scrape the URL. {e}"

def enhance_with_isabella_voice(raw_text: str) -> str:
    """Takes raw text and reframes it using the proprietary Isabella brand voice."""
    
    # This is the 'soul' of your brand. It's a powerful, detailed prompt.
    isabella_prompt = """
    Act as 'Isabella de Fortibus', the Sovereign Curator. Your voice is timeless, authoritative, and poetic. 
    Transform the following raw text about a place or event into an alluring, premium narrative. 
    Focus on the feeling, the legacy, and the unique experience. 
    Preserve all key factual details (like names, times, and activities) but weave them into a compelling story. 
    Eliminate all boilerplate, marketing jargon, and repetitive phrasing.

    Raw Text:
    ---
    {raw_text}
    ---

    Your Enhanced Narrative:
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": isabella_prompt.format(raw_text=raw_text)}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: Could not enhance the text. {e}"