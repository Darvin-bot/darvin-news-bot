import feedparser
import os
import requests
from datetime import datetime, timedelta
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Источники новостей
RSS_FEEDS = [
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

# Ключевые слова для фильтрации
KEYWORDS = [
    "FDA", "clinical", "approval", "acquisition", "buyback", "merger", "lawsuit",
    "investigation", "partnership", "guidance", "bankruptcy", "license", "AI", "chip",
    "short squeeze", "IPO", "revenue", "earnings", "fraud", "resignation", "recall",
    "warning letter", "delisting", "DOJ", "SEC", "class action", "revoked", "terminated",
    "settlement", "fine", "probe", "layoffs"
]

# Telegram конфигурация
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def contains_keyword(text):
    if not text:
        return False
    text = text.lower()
    return any(keyword.lower() in text for keyword in KEYWORDS)

def format_message(entry):
    title = entry.get("title", "No title")
    link = entry.get("link", "")
    published = entry.get("published", "")
    summary = entry.get("summary", "")

    # Поиск $тикера
    ticker = ""
    for word in summary.split():
        if word.startswith("$") and len(word) < 8:
            ticker = word
            break

    message = f"📰 <b>{title}</b>\n"
    if ticker:
        message += f"📈 {ticker}\n"
    message += f"{summary[:250]}...\n🔗 {link}"
    return message

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    response = requests.post(url, json=payload)
    logging.info(f"Sent: {response.status_code} - {message[:50]}")

def fetch_and_filter_news():
    logging.info("Start fetching feeds...")
    now = datetime.utcnow()
    recent_limit = now - timedelta(hours=6)

    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            pub_date = entry.get("published_parsed")
            if not pub_date:
                continue
            published = datetime(*pub_date[:6])
            if published < recent_limit:
                continue

            title = entry.get("title", "")
            summary = entry.get("summary", "")
            if contains_keyword(title) or contains_keyword(summary):
                message = format_message(entry)
                send_to_telegram(message)

if __name__ == "__main__":
    fetch_and_filter_news()
