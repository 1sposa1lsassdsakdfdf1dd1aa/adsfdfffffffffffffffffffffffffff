from fastapi import FastAPI, Request
import requests
from fastapi.responses import RedirectResponse

app = FastAPI()

@app.get("/api/stream/{channel}.m3u8")
async def get_stream(channel: str, request: Request):
    try:
        # Construct the play URL with the stream ID
        play_url = f"https://secureplayer.sportstvn.com/token.php?stream={channel}"

        # Fetch the token with required headers
        headers = {"Referer": "https://sportstvn.com/"}
        response = requests.get(play_url, headers=headers)

        if response.status_code != 200:
            return {"error": "Failed to fetch token."}

        # Extract token using regex
        import re
        match = re.search(r"token=([a-f0-9\-]+)", response.text)
        if not match:
            return {"error": "Token not found in the response."}

        token = match.group(1)
        m3u8_url = f"https://cdn.sturls.com/{channel}/index.m3u8?token={token}"

        # Redirect to the final M3U8 URL
        return RedirectResponse(url=m3u8_url)

    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}
