import feedparser
import requests
from bs4 import BeautifulSoup
import csv
import random

def collect_from_feeds(feed_urls, max_articles=100):
    articles = []
    for url in feed_urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if len(articles) >= max_articles:
                break
            link = entry.get('link')
            try:
                resp = requests.get(link, headers={
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) " 
                  "AppleWebKit/537.36 (KHTML, like Gecko) " 
                  "Chrome/100.0.0.0 Safari/537.36"
})

                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, "html.parser")
                paragraphs = soup.find_all("p")
                text = "\n".join(p.get_text() for p in paragraphs).strip()
                if len(text) > 50:  # skip very short pieces
                    articles.append(text)
            except Exception:
                continue
        if len(articles) >= max_articles:
            break
    random.shuffle(articles)
    return articles

# 1. Real‑news RSS/Atom feeds
real_feeds = [
    "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml",
    "http://rss.cnn.com/rss/edition.rss"
]

# Collect 100 articles each
real_texts = collect_from_feeds(real_feeds, max_articles=100)

# Write real-news CSV
with open("real_news.csv", "w", newline="", encoding="utf-8") as f_real:
    writer = csv.DictWriter(f_real, fieldnames=["text", "class"])
    writer.writeheader()
    for txt in real_texts:
        writer.writerow({"text": txt, "class": 1})


print(f"Wrote {len(real_texts)} real-news articles to real_news.csv")
