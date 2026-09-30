import csv
import json
import feedparser

feeds = {
    "Lenta.ru": "https://lenta.ru/rss/news",
    "RT": "https://russian.rt.com/rss",
}


def get_news(url):
    feed = feedparser.parse(url, agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
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


def main():
    for name, url in feeds.items():
        print(f"\n=== {name} ===")

        news = get_news(url)
        print(f"Найдено новостей: {len(news)}")

        if not news:
            print("Лента пуста. Возможно, изменился адрес RSS.")
            continue

        for n in news[:5]:
            print(f"• {n['title']}")
            print(f"  {n['link']}")

        save_csv(news, f"{name}.csv")
        save_json(news, f"{name}.json")
        print(f"Сохранено в {name}.csv и {name}.json")


if __name__ == "__main__":
    main()