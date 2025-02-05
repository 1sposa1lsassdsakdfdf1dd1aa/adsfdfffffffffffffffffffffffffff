from fastapi import FastAPI, Request
import requests
import re

app = FastAPI()

@app.get("/api/playlist.m3u")
async def get_stream(request: Request):
    # Define a list of channels and their details (name, id, logo)
    channels = [
        {"name": "SSC | Extra 02", "id": "Extra02", "logo": ""},
        {"name": "SSC | Extra 01", "id": "Extra01", "logo": ""},
        {"name": "Sky Sport 03", "id": "SkySport03", "logo": ""},
        {"name": "Sky Sport 02", "id": "SkySport02", "logo": ""},
        {"name": "Sky Sport 01", "id": "SkySport01", "logo": ""},
        {"name": "Super Sports Cricket", "id": "SuperSportsCricket", "logo": ""},
        {"name": "DAZN 02", "id": "DAZN02", "logo": ""},
        {"name": "DAZN 01", "id": "DAZN01", "logo": ""},
        {"name": "BPL Special", "id": "BPLSpecial", "logo": ""},
        {"name": "T Sports", "id": "TSports", "logo": ""},
        {"name": "Sony Sports Ten 05", "id": "SonySportsTen01", "logo": ""},
        {"name": "Sony Sports Ten 03", "id": "SonySportsTen02", "logo": ""},
        {"name": "Sony Sports Ten 02", "id": "SonySportsTen03", "logo": ""},
        {"name": "Sony Sports Ten 01", "id": "SonySportsTen05", "logo": ""},
        {"name": "Star Sports Select 02", "id": "StarSportsSelect02", "logo": ""},
        {"name": "Star Sports Select 01", "id": "StarSportsSelect01", "logo": ""},
        {"name": "Star Sports 02", "id": "StarSports02", "logo": ""},
        {"name": "Star Sports 01", "id": "StarSports01", "logo": ""},
        {"name": "TNT Sports 04", "id": "TNTSports04", "logo": ""},
        {"name": "TNT Sports 03", "id": "TNTSports03", "logo": ""},
        {"name": "TNT Sports 02", "id": "TNTSports02", "logo": ""},
        {"name": "TNT Sports 01", "id": "TNTSports01", "logo": ""},
        {"name": "Bein Sports 04", "id": "BeinSports04", "logo": ""},
        {"name": "Bein Sports 03", "id": "BeinSports03", "logo": ""},
        {"name": "Bein Sports 02", "id": "BeinSports02", "logo": ""},
        {"name": "Bein Sports 01", "id": "BeinSports01", "logo": ""},
        {"name": "PTV Sports", "id": "PTVSports", "logo": ""},
        {"name": "A Sports", "id": "ASports", "logo": ""},
        {"name": "Sports 18", "id": "Sports18", "logo": ""},
        {"name": "Sky Sports Cricket", "id": "SkySportsCricket", "logo": ""},
        {"name": "Fox Cricket 501", "id": "FoxSports501", "logo": ""},
        {"name": "SSC 01", "id": "SSC1-SaudiArab", "logo": ""}

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
                        "logo": channel["logo"],
                        "url": "XFIREFLIX",
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
