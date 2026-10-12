
from src.news_collector import fetch_news
from src.predict import predict_news
from src.database import create_database, save_article, article_exists


def classify_articles(limit=5):

    # Collect articles from RSS feeds
    articles = fetch_news(limit=limit)

    classified_articles = []
    seen_links = set()

    for article in articles:

        # Get the article link
        link = article["link"]

        # Skip articles without links or duplicates in the feed
        if not link or link in seen_links:
            continue

        seen_links.add(link)

        # Skip articles already saved in the database
        if article_exists(link):
            continue

        # Get the article headline
        text = article["title"]

        if not text.strip():
            continue

        # Classify the headline using DistilBERT
        result = predict_news(text)

        # Combine article information with prediction
        classified_article = {
            "title": article["title"],
            "source": article["source"],
            "link": article["link"],
            "published": article["published"],
            "predicted_category": result["prediction"],
            "probabilities": result["probabilities"]
        }

        classified_articles.append(classified_article)

    return classified_articles


def run_pipeline(limit=5):

    # Create the database if it doesn't exist
    create_database()

    # Collect and classify new articles
    results = classify_articles(limit=limit)

    saved_count = 0

    print(f"\nTotal new articles classified: {len(results)}\n")

    for article in results:

        # Save the article to SQLite
        if save_article(article):
            saved_count += 1

        # Get the predicted category probability
        confidence = article["probabilities"][
            article["predicted_category"]
        ]

        # Display results
        print("Title:", article["title"])
        print("Source:", article["source"])
        print("Prediction:", article["predicted_category"])
        print(f"Model confidence: {confidence:.2%}")
        print("Link:", article["link"])
        print("-" * 60)

    # Pipeline summary
    print("\nPipeline completed!")
    print(f"Articles classified: {len(results)}")
    print(f"New articles saved: {saved_count}")

    return {
        "classified": len(results),
        "saved": saved_count
    }


if __name__ == "__main__":
    run_pipeline(limit=5)
