import pandas as pd
import numpy as np


class DataProcessor:
    @staticmethod
    def clean_category_sales(df: pd.DataFrame) -> pd.DataFrame:
        """Cleans category sales data using Pandas and NumPy."""
        df = df.copy()

        df["category_name"] = df["category_name"].fillna("Uncategorized")

        df["total_revenue"] = np.round(df["total_revenue"].values, 2)
        df["average_order_value"] = np.round(df["average_order_value"].values, 2)

        total_sum = np.sum(df["total_revenue"])
        df["revenue_share_pct"] = np.round((df["total_revenue"] / total_sum) * 100, 2)

        return df

    @staticmethod
    def process_seller_rankings(df: pd.DataFrame) -> pd.DataFrame:

        df = df.copy()
        df["total_revenue"] = np.round(df["total_revenue"].values, 2)
        return df
