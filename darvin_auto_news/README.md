# Darvin Market News Auto Bot

Этот проект автоматически собирает важные новости и отправляет их в Telegram-канал @darvinmarketnews через @darvinnews_bot.

### Источники новостей:

1. https://seekingalpha.com/market-news/trending
2. https://www.sec.gov/news/pressreleases
3. https://www.fda.gov/news-events/fda-newsroom/press-announcements
4. https://www.semiaccurate.com/
5. https://www.insidermonkey.com/blog/category/news/

### Расписание (NY Time)

- 03:30 NY — за 30 мин до премаркета
- 08:30 NY — за час до открытия рынка
- 15:00 NY — за час до закрытия

### Установка

1. Клонируй репозиторий или загрузи ZIP-архив.
2. Перейди в Settings → Secrets and variables → Actions и добавь:
   - `BOT_TOKEN`: токен твоего Telegram-бота
   - `CHAT_ID`: `@darvinmarketnews`
3. Всё готово — новости будут отправляться автоматически.