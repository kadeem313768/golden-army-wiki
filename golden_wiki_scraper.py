import requests
from bs4 import BeautifulSoup

# 目標網站
base_url = "https://golden-army.fandom.com"

# 起始頁面
start_page = "/wiki/Gold_in_practice"

# 已抓取頁面
visited = set()

# 儲存資料
all_pages = {}

def scrape_page(relative_url):
    if relative_url in visited:
        return
    visited.add(relative_url)

    url = base_url + relative_url
    response = requests.get(url)
    if response.status_code != 200:
        print(f"無法訪問 {url}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # 抓標題和正文
    title = soup.find('h1').text.strip()
    content = "\n".join([p.text.strip() for p in soup.select('.mw-parser-output > p') if p.text.strip()])

    print(f"抓取頁面: {title}")

    all_pages[title] = content

    # 找子頁面
    for link in soup.select('.mw-parser-output a[href^="/wiki/"]'):
        sub_url = link.get('href')
        if ':' not in sub_url:  # 避免抓到特殊頁面（比如檔案頁、討論頁）
            scrape_page(sub_url)

# 開始抓取
scrape_page(start_page)

# 把結果寫入檔案
with open('golden_army_wiki.txt', 'w', encoding='utf-8') as f:
    for title, content in all_pages.items():
        f.write(f"### {title}\n{content}\n\n")
