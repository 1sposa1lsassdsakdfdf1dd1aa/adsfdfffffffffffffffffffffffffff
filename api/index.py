from fastapi import FastAPI, Request
import requests
import re

app = FastAPI()

@app.get("/api/playlist.m3u")
async def get_stream(request: Request):
    # Define a list of channels and their details (name, id, logo)
channels = [
        {"name": "SSC | Extra 02", "id": "Extra02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/SSC-Extra-2-300x188.png"},
        {"name": "SSC | Extra 01", "id": "Extra01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/SSC-Extra-1-300x188.png"},
        {"name": "Sky Sport 03", "id": "SkySport03", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Sky-Sport03.png"},
        {"name": "Sky Sport 02", "id": "SkySport02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Sky-Sport02.png"},
        {"name": "Sky Sport 01", "id": "SkySport01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Sky-Sport01.png"},
        {"name": "Super Sports Cricket", "id": "SuperSportsCricket", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Super-Sports-Cricket.png"},
        {"name": "DAZN 02", "id": "DAZN02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/DAZN-2.png"},
        {"name": "DAZN 01", "id": "DAZN01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/DAZN-1.png"},
        {"name": "BPL Special", "id": "BPLSpecial", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/BPL-Special-300x169.png"},
        {"name": "T Sports", "id": "TSports", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/T-Sports.jpg"},
        {"name": "Sony Sports Ten 05", "id": "SonySportsTen01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/sonysports5.png"},
        {"name": "Sony Sports Ten 03", "id": "SonySportsTen02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/sonysports3.png"},
        {"name": "Sony Sports Ten 02", "id": "SonySportsTen03", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/sonysports2.png"},
        {"name": "Sony Sports Ten 01", "id": "SonySportsTen05", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/sonysports1.png"},
        {"name": "Star Sports Select 02", "id": "StarSportsSelect02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/imgstarsports2.png/"},
        {"name": "Star Sports Select 01", "id": "StarSportsSelect01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/starsports1.png"},
        {"name": "Star Sports 02", "id": "StarSports02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/star-Sportsselect2-HD.jpg"},
        {"name": "Star Sports 01", "id": "StarSports01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/star-Sportsselect1-HD.jpg"},
        {"name": "TNT Sports 04", "id": "TNTSports04", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/TNT-Sports-4.png"},
        {"name": "TNT Sports 03", "id": "TNTSports03", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/TNT-Sports-3.png"},
        {"name": "TNT Sports 02", "id": "TNTSports02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/TNT-Sports-2.png"},
        {"name": "TNT Sports 01", "id": "TNTSports01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/TNT-Sports-1.png"},
        {"name": "Bein Sports 04", "id": "BeinSports04", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Bein-Sports4-HD.png"},
        {"name": "Bein Sports 03", "id": "BeinSports03", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Bein-Sports3-HD.png"},
        {"name": "Bein Sports 02", "id": "BeinSports02", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Bein-Sports2-HD.png"},
        {"name": "Bein Sports 01", "id": "BeinSports01", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Bein-Sports1-HD.png"},
        {"name": "PTV Sports", "id": "PTVSports", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/PTV-Sports-HD.png"},
        {"name": "A Sports", "id": "ASports", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/A-Sports.jpg"},
        {"name": "Sports 18", "id": "Sports18", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Sports18.png"},
        {"name": "Sky Sports Cricket", "id": "SkySportsCricket", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Sky-Sports-Cricket.png"},
        {"name": "Fox Cricket 501", "id": "FoxSports501", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/Fox-Cricket-501-300x188.png"},
        {"name": "SSC 01", "id": "SSC1-SaudiArab", "logo": "https://raw.githubusercontent.com/HelloPeopleTv4you/IPTV-Playlist/406da1fce47b6a0b713d4893c7c633b4bee2b645/img/SSC1.jpg"}
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
                        "logo": channel["logo"],
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
