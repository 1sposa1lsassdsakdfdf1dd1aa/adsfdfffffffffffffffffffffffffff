from fastapi import FastAPI, Request
import requests
import re

app = FastAPI()

@app.get("/api/stream")
async def get_stream(request: Request):
    # Define a list of channels and their details
    channels = [
        {"name": "SSC | Extra 02", "id": "Extra02"},
        {"name": "Sky Sport 03", "id": "SkySport03"},
        {"name": "Sky Sport 02", "id": "SkySport02"},
        {"name": "Sky Sport 01", "id": "SkySport01"},
        {"name": "DAZN 02", "id": "DAZN02"},
        {"name": "DAZN 01", "id": "DAZN01"},
        {"name": "SSC 01", "id": "SSC1-SaudiArab"},
        {"name": "BPL Special", "id": "BPLSpecial"},
        {"name": "T Sports", "id": "TSports"},
        {"name": "Sony Sports Ten 03", "id": "SonySportsTen03"}
    ]

    result = []

    for channel in channels:
        try:
            # Construct the play URL
            stream_url = f"https://secureplayer.sportstvn.com/token.php?stream={channel['id']}"

            # Set headers to mimic a real browser request
            headers = {
                "Referer": "https://sportstvn.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }

            # Fetch the token using requests
            response = requests.get(stream_url, headers=headers)

            if response.status_code == 200:
                # Extract the token using regex
                match = re.search(r"token=([a-f0-9\-]+)", response.text)
                if match:
                    token = match.group(1)
                    link = f"https://cdn.sturls.com/{channel['id']}/index.mpd?token={token}&remote=no_check_ip"
                    result.append({
                        "name": channel["name"],
                        "logo": "",  # Add the actual logo URL if available
                        "url": f"https://sportstvn.com/channel/{channel['id'].lower()}/",
                        "stream_url": stream_url,
                        "link": link,
                        "referer": "https://secureplayer.sportstvn.com/"
                    })
                else:
                    result.append({"name": channel["name"], "error": "Token not found"})
            else:
                result.append({"name": channel["name"], "error": f"Failed to fetch token. Status code: {response.status_code}"})
        
        except Exception as e:
            result.append({"name": channel["name"], "error": f"Internal Server Error: {str(e)}"})

    return result
