import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.iptvregion.eu.org/search/label/M3U?m=1"

def get_m3u_links():
    response = requests.get(BASE_URL)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [a["href"] for a in soup.find_all("a", href=True) if ".m3u" in a["href"]]
    return links[:5]  # return top 5 links

def save_to_file(links, filename="opale.m3u"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for link in links:
            f.write(f"#EXTINF:-1,{link}\n{link}\n")

if __name__ == "__main__":
    links = get_m3u_links()
    save_to_file(links)
