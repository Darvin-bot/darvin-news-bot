import requests, feedparser, os
from datetime import datetime
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
NY_TIME_NOW = datetime.utcnow().timestamp() - 4 * 3600

KEYWORDS = [
    "FDA", "clinical", "approval", "acquisition", "buyback", "merger", "lawsuit",
    "investigation", "partnership", "guidance", "bankruptcy", "license", "AI", "chip", "short squeeze"
]

FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
    "https://seekingalpha.com/market-news/trending.xml",
    "https://www.semiaccurate.com/feed/",
    "https://www.insidermonkey.com/blog/category/news/feed/"
]

def clean_html(text):
    return BeautifulSoup(text, "html.parser").get_text()

def send_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True
    }
    requests.post(url, json=payload)

def is_important(entry):
    title = entry.get("title", "").lower()
    summary = entry.get("summary", "").lower()
    return any(k.lower() in title + summary for k in KEYWORDS)

def format_news(entry):
    title = clean_html(entry.get("title", ""))
    link = entry.get("link", "")
    summary = clean_html(entry.get("summary", ""))[:300]
    return f"🚨 *{title}*\n{summary}\n[Read more]({link})"

def main():
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            if is_important(entry):
                text = format_news(entry)
                send_telegram(text)

if __name__ == "__main__":
    main()
