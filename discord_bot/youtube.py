import json
import os
from urllib.request import urlopen
from random import randint
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("YOUTUBE_TOKEN")
url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=50&q=lofi%20music&type=video&key={api_key}"


def search_youtube():
    result = urlopen(url)
    result = json.loads(result.read())
    item_index = randint(0, len(result) - 1)
    item = result["items"][item_index]

    yield f"https://www.youtube.com/watch?v={item["id"]["videoId"]}"


__all__ = ["search_youtube"]


if __name__ == "__main__":
    search_youtube()