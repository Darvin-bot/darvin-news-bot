import requests
import time
from datetime import datetime
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

NEWS_SOURCES = [
    "https://seekingalpha.com/market-news/trending",
    "https://www.insidermonkey.com/blog/category/news/",
    "https://www.semiaccurate.com/",
    "https://www.sec.gov/news/pressreleases",
    "https://www.fda.gov/news-events/fda-newsroom/press-announcements"
]

def get_mocked_news():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    return [
        f"🚨 Sample news headline 1 at {now} [$TSLA]\nhttps://example.com/1 🔥 HIGH IMPACT",
        f"🧪 Sample biotech news 2 at {now} [$BIIB]\nhttps://example.com/2",
    ]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=payload)
    return response.json()

def main():
    news_items = get_mocked_news()
    for news in news_items:
        send_telegram_message(news)
        time.sleep(1)

if __name__ == "__main__":
    main()