from fastapi import FastAPI, Request
import requests
import re

app = FastAPI()

@app.get("/api/stream")
async def get_stream(request: Request):
    channel = request.query_params.get("id")
    
    if not channel:
        return {"error": "No channel specified. Use /api/stream?id=yourChannelID"}

    try:
        # Construct the stream URL
        stream_url = f"https://secureplayer.sportstvn.com/token.php?stream={channel}"

        headers = {
            "Referer": "https://sportstvn.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Request the token from the stream URL
        response = requests.get(stream_url, headers=headers)

        if response.status_code != 200:
            return {"error": f"Failed to fetch token. Status code: {response.status_code}"}

        # Extract the token from the response
        match = re.search(r"token=([a-f0-9\-]+)", response.text)
        if not match:
            return {"error": "Token not found in the response."}

        token = match.group(1)
        link = f"https://cdn.sturls.com/{channel}/index.mpd?token={token}&remote=no_check_ip"

        # Return the output in the desired format
        return {
            "name": f"{channel.replace('-', ' ').title()}",
            "logo": "",
            "url": f"https://sportstvn.com/channel/{channel.lower().replace(' ', '-')}/",
            "stream_url": stream_url,
            "link": link,
            "referer": "https://secureplayer.sportstvn.com/"
        }

    except Exception as e:
        return {"error": f"Internal Server Error: {str(e)}"}
