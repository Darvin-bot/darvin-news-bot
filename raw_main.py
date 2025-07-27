import requests, feedparser, os
from bs4 import BeautifulSoup

TELEGRAM_BOT_TOKEN = os.getenv("RAW_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("RAW_TELEGRAM_CHAT_ID")

FEEDS = [
    "https://www.sec.gov/news/pressreleases.rss",
    "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
    "https://seekingalpha.com/market-news/trending.xml",
    "https://www.semiaccurate.com/feed/",
    "https://www.insidermonkey.com/blog/category/news/feed/",
    "https://finance.yahoo.com/news/rssindex",
    "https://www.marketwatch.com/rss",
    "https://www.prnewswire.com/rss/health-latest-news.rss",
    "https://www.globenewswire.com/RssFeed/newsroom/All",
    "https://www.fiercebiotech.com/rss.xml"
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

def format_news(entry):
    title = clean_html(entry.get("title", ""))
    link = entry.get("link", "")
    summary = clean_html(entry.get("summary", ""))[:300]
    return f"📰 *{title}*\n{summary}\n[Read more]({link})"

def main():
    for url in FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries[:5]:
            text = format_news(entry)
            send_telegram(text)

if __name__ == "__main__":
    main()
