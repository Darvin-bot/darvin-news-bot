import feedparser
import os
import requests
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

KEYWORDS = [
    "FDA", "clinical", "approval", "acquisition", "buyback", "merger", "lawsuit",
    "investigation", "partnership", "guidance", "bankruptcy", "license", "AI", "chip",
    "short squeeze", "IPO", "revenue", "earnings", "fraud", "resignation", "recall",
    "warning letter", "delisting", "DOJ", "SEC", "class action", "revoked", "terminated",
    "settlement", "fine", "probe", "layoffs"
]

FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
    "https://seekingalpha.com/market-news/trending.xml",
    "https://finance.yahoo.com/news/rssindex",
    "https://www.marketwatch.com/rss",
    "https://www.prnewswire.com/rss/health-latest-news.rss",
    "https://www.globenewswire.com/RssFeed/newsroom/All",
    "https://www.fiercebiotech.com/rss.xml"
]

def clean(text):
    return BeautifulSoup(text, "html.parser").get_text()

def contains_keywords(text):
    text = text.lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)

def format_entry(entry):
    title = clean(entry.get("title", ""))
    summary = clean(entry.get("summary", ""))
    link = entry.get("link", "")
    return f"🚨 *{title}*\n{summary[:250]}...\n[Read more]({link})"

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    requests.post(url, json=payload)

def main():
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:8]:
            text = clean(entry.get("title", "") + " " + entry.get("summary", ""))
            if contains_keywords(text):
                message = format_entry(entry)
                send_to_telegram(message)

if __name__ == "__main__":
    main()
