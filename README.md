# 📰 Darvin Market News Bot

Автоматическая рассылка новостей 3 раза в день через GitHub Actions в Telegram-канал.

## 📦 Инструкция

1. Создай репозиторий на GitHub (private/public — по желанию)
2. Залей туда эти файлы
3. Перейди в Settings > Secrets > Actions и добавь два секрета:
   - `TELEGRAM_TOKEN` — токен от @darvinnews_bot
   - `TELEGRAM_CHAT_ID` — ID канала (@darvinmarketnews)
4. Готово. Бот будет автоматически публиковать важные новости 3 раза в день

## 🕒 Расписание по NY:

- 03:30 AM NY
- 08:30 AM NY
- 03:00 PM NY

## 📡 Источники:

1. [SEC Press Releases](https://www.sec.gov/news/pressreleases.rss)
2. [FDA Press Releases](https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml)
3. [Seeking Alpha Trending](https://seekingalpha.com/market-news/trending)
4. [SemiAccurate](https://www.semiaccurate.com/)
5. [Insider Monkey News](https://www.insidermonkey.com/blog/category/news/)

Фильтрация по ключевым словам: FDA, buyback, AI, clinical, acquisition и др.