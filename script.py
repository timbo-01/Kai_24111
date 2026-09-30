import asyncio
import csv
import json

import aiohttp
import feedparser

feeds = {
    "Lenta.ru": "https://lenta.ru/rss/news",
    "RT": "https://russian.rt.com/rss/news",
}

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


def parse_feed(text):
    feed = feedparser.parse(text)
    news = []
    for entry in feed.entries:
        news.append({
            "title": entry.get("title", ""),
            "link": entry.get("link", ""),
            "published": entry.get("published", ""),
        })
    return news


def save_csv(news, filename):
    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "link", "published"])
        writer.writeheader()
        writer.writerows(news)


def save_json(news, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(news, f, ensure_ascii=False, indent=2)


async def process_feed(session, name, url):
    print(f"\n {name} ")

    text = await fetch(session, url)
    news = parse_feed(text)
    print(f"Найдено новостей: {len(news)}")

    if not news:
        print("Лента пуста. Возможно, изменился адрес RSS.")
        return

    for n in news[:5]:
        print(f"• {n['title']}")
        print(f"  {n['link']}")

    save_csv(news, f"{name}.csv")
    save_json(news, f"{name}.json")
    print(f"Сохранено в {name}.csv и {name}.json")


async def main():
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        tasks = [
            process_feed(session, name, url)
            for name, url in feeds.items()
        ]
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())