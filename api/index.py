from fastapi import FastAPI, Request
import requests
from fastapi.responses import RedirectResponse
import re

app = FastAPI()

@app.get("/api/stream")
async def get_stream(request: Request):
    # Get the 'id' parameter from the URL
    channel = request.query_params.get("id")
    
    if not channel:
        return {"error": "No channel specified. Use /api/stream?id=yourChannelID"}

    try:
        # Construct the play URL with the stream ID (same as PHP code)
        play_url = f"https://secureplayer.sportstvn.com/token.php?stream={channel}"

        # Set headers to mimic a real browser request (similar to PHP cURL headers)
        headers = {
            "Referer": "https://sportstvn.com/",  # Referer header to simulate a valid request source
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Fetch the token using requests
        response = requests.get(play_url, headers=headers)

        if response.status_code != 200:
            return {"error": "Failed to fetch token. Status code: " + str(response.status_code)}

        # Extract the token using regex, same as PHP
        match = re.search(r"token=([a-f0-9\-]+)", response.text)
        if not match:
            return {"error": "Token not found in the response."}

        token = match.group(1)
        m3u8_url = f"https://cdn.sturls.com/{channel}/index.m3u8?token={token}"

        # Redirect the user to the new M3U8 URL
        return RedirectResponse(url=m3u8_url)

    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}
