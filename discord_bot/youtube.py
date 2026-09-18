from urllib.request import urlopen, Request
import json



api_key = "AIzaSyBribM9vxgqR3zEW3-jW47CLcgOMXN_jRs"
url = f"https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=lofi%20music&type=video&key={api_key}"

def search_youtube():
    result = urlopen(url)
    result = json.loads(result.read())

    for item in result["items"]:
        print(f"https://www.youtube.com/watch?v={item["id"]["videoId"]}")


if __name__ == "__main__":
    search_youtube()