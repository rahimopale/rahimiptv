import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.iptvregion.eu.org/search/label/M3U?m=1"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_post_links():
    res = requests.get(BASE_URL, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")
    posts = soup.select("a[href*='/20']")  # rough filter for post links
    links = [a["href"] for a in posts if a["href"].startswith("https://www.iptvregion.eu.org")]
    return links[:5]

def extract_m3u_from_post(url):
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.content, "html.parser")
    m3u_links = [a["href"] for a in soup.find_all("a", href=True) if a["href"].endswith(".m3u") or ".m3u?" in a["href"]]
    return m3u_links[:5]

def save_all_links(all_links, filename="opale.m3u"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in all_links:
            f.write(f"#EXTINF:-1,{link}\n{link}\n")

if __name__ == "__main__":
    all_links = []
    posts = get_post_links()
    for post in posts:
        links = extract_m3u_from_post(post)
        all_links.extend(links)
    save_all_links(all_links)
