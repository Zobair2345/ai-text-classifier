from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from src.news_pipeline import run_pipeline


def scheduled_news_collection():
    print(f"\nStarting scheduled collection: {datetime.now()}")

    try:
        result = run_pipeline(limit=5)

        print(f"New articles classified: {result['classified']}")
        print(f"New articles saved: {result['saved']}")

    except Exception as error:
        print(f"Scheduled collection failed: {error}")


if __name__ == "__main__":

    scheduler = BlockingScheduler()

    scheduler.add_job(
        scheduled_news_collection,
        trigger="interval",
        hours=1,
        id="news_collection",
        max_instances=1,
        coalesce=True
    )

    print("Research news scheduler started.")
    print("News collection will run every hour.")

    # Run once immediately
    scheduled_news_collection()

    # Continue running scheduled jobs
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Scheduler stopped.")