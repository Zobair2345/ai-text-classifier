import feedparser

RSS_FEEDS = {
    "BBC World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "BBC Business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "BBC Technology": "https://feeds.bbci.co.uk/news/technology/rss.xml"
}


def fetch_news(limit=5):
    articles = []

    for source, url in RSS_FEEDS.items():

        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
         print(f"Unable to read feed: {source}")
         print(f"Error: {feed.bozo_exception}")
         print(f"HTTP status: {feed.get('status', 'Unknown')}")
         print("-" * 50)
         continue
    
        for entry in feed.entries[:limit]:

            article = {
                "title": entry.get("title", ""),
                "summary": entry.get("summary", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": source
            }

            articles.append(article)

    return articles


if __name__ == "__main__":

    articles = fetch_news(limit=5)

    print(f"Total articles collected: {len(articles)}")

    for article in articles:
        print("Source:", article["source"])
        print("Title:", article["title"])
        print("Link:", article["link"])
        print("-" * 50)