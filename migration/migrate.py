import os
from database.connection import get_engine, logger
from config.settings import DATASET_DIR
import pandas as pd

FILE_TO_TABLES = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_products_dataset.csv": "products",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "olostproduct_category_name_translation.csv": "category_name_translation",
}


def migrate_csv_to_db():
    """Reads CSV datasets and bulk loads them into PostgreSQL."""
    engine = get_engine()

    for file_name, table_name in FILE_TO_TABLES.items():
        file_path = os.path.join(DATASET_DIR, file_name)
        if not os.path.exists(file_path):
            logger.warning(f"File skipped (not found): {file_path}")
            continue

        logger.info(f"Ingesting '{file_name}' into table '{table_name}'...")
        df = pd.read_csv(file_path)

        # Load into PostgreSQL using chunks for memory efficiency
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi",
        )
        logger.info(f"Successfully loaded {len(df)} rows into '{table_name}'.")


if __name__ == "__main__":
    migrate_csv_to_db()
