import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://golden-army.fandom.com"
START_PAGE = "/wiki/Gold_in_practice"
visited = set()
wiki_data = {}

def crawl_page(path):
    if path in visited:
        return
    visited.add(path)

    url = BASE_URL + path
    print(f"Crawling: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 抓取頁面標題和內容
        title_tag = soup.find("h1")
        if title_tag:
            title = title_tag.text.strip()
            content = []
            paragraphs = soup.find_all("p")
            for p in paragraphs:
                text = p.text.strip()
                if text:
                    content.append(text)
            wiki_data[title] = "\n".join(content)

        # 找到所有指向內部Wiki的連結
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if href.startswith("/wiki/") and not href.startswith("/wiki/Special:"):
                crawl_page(href)

        time.sleep(0.5)
    except Exception as e:
        print(f"Failed to crawl {url}: {e}")

def scrape_wiki():
    crawl_page(START_PAGE)
    return wiki_data
