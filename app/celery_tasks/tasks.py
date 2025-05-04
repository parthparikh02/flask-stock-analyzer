from app import celery_app, create_app
from app.services.stock_fetcher import fetch_and_store_stock_data
from datetime import datetime
import os

flask_app = create_app(os.getenv("FLASK_CONFIG") or "dev")

@celery_app.task(name='tasks.fetch_and_store_task')
def fetch_and_store_task():
    try:

        print(f"All symbol data fetching started at: {datetime.now()}")

        with flask_app.app_context():
            fetch_and_store_stock_data()

        print(f"All symbol data fetching finished at: {datetime.now()}")

    except Exception as e:
        print(f"Error in fetching and storing data for all symbols: {e}")
