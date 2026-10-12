import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "news.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def create_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT,
                link TEXT UNIQUE NOT NULL,
                published TEXT,
                predicted_category TEXT,
                confidence REAL,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

    print("Database ready!")

def save_article(article):

    confidence = article["probabilities"][
        article["predicted_category"]
    ]

    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO articles (
                title,
                source,
                link,
                published,
                predicted_category,
                confidence
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                article["title"],
                article["source"],
                article["link"],
                article["published"],
                article["predicted_category"],
                confidence
            )
        )

        return cursor.rowcount == 1    

import pandas as pd



def get_articles():

    with get_connection() as conn:
        articles = pd.read_sql_query(
            """
            SELECT
                title,
                source,
                predicted_category,
                confidence,
                published,
                collected_at,
                link
            FROM articles
            ORDER BY collected_at DESC, id DESC
            """,
            conn
        )

    return articles


def article_exists(link):

    with get_connection() as conn:
        result = conn.execute(
            "SELECT 1 FROM articles WHERE link = ? LIMIT 1",
            (link,)
        ).fetchone()

    return result is not None


if __name__ == "__main__":
    create_database()
