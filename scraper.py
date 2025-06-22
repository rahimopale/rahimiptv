import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.iptvregion.eu.org/search/label/M3U?m=1"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com"
}

def get_m3u_links():
    try:
        response = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        links = [a["href"] for a in soup.find_all("a", href=True) if ".m3u" in a["href"]]
        return links[:5]  # Return top 5 M3U links
    except Exception as e:
        print("Failed to retrieve M3U links:", e)
        return []

def save_to_file(links, filename="opale.m3u"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in links:
            f.write(f"#EXTINF:-1,{link}\n{link}\n")

if __name__ == "__main__":
    links = get_m3u_links()
    save_to_file(links)
