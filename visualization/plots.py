import os
import matplotlib.pyplot as plt
import pandas as pd
from config.settings import PLOTS_DIR

os.makedirs(PLOTS_DIR, exist_ok=True)


class SalesVisualizer:
    @staticmethod
    def plot_top_categories(df: pd.DataFrame):
        top_10 = df.head(10)
        plt.figure(figsize=(10, 5))
        plt.barh(top_10["category_name"], top_10["total_revenue"], color="#2b5c8f")
        plt.xlabel("Total Revenue ($)")
        plt.title("Top 10 Product Categories by Revenue")
        plt.gca().invert_yaxis()
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "01_top_categories.png"), dpi=300)
        plt.close()

    @staticmethod
    def plot_revenue_vs_orders(df: pd.DataFrame):
        plt.figure(figsize=(8, 5))
        plt.scatter(df["total_orders"], df["total_revenue"], color="#e056fd", alpha=0.7)
        plt.xlabel("Total Orders")
        plt.ylabel("Total Revenue ($)")
        plt.title("Category Revenue vs. Order Volume")
        plt.grid(True, linestyle="--", alpha=0.5)
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "02_revenue_vs_orders.png"), dpi=300)
        plt.close()

    @staticmethod
    def plot_aov_distribution(df: pd.DataFrame):
        plt.figure(figsize=(8, 5))
        plt.hist(df["average_order_value"], bins=15, color="#2ed573", edgecolor="black")
        plt.xlabel("Average Order Value ($)")
        plt.ylabel("Category Count")
        plt.title("Distribution of Average Order Value")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "03_aov_distribution.png"), dpi=300)
        plt.close()

    @staticmethod
    def plot_top_sellers_by_state(df: pd.DataFrame):
        state_counts = df["seller_state"].value_counts().head(6)

        # Custom color palette for distinct visual separation
        colors = ["#ff6b6b", "#4ecdc4", "#ffe66d", "#1a535c", "#f7fff7", "#ff9f43"]

        plt.figure(figsize=(7, 7))

        # Create Donut Plot
        wedges, texts, autotexts = plt.pie(
            state_counts.values,
            labels=state_counts.index,
            autopct="%1.1f%%",
            startangle=140,
            colors=colors,
            pctdistance=0.75,
            wedgeprops=dict(width=0.4, edgecolor="white", linewidth=2),
        )

        # Style text inside wedges
        for autotext in autotexts:
            autotext.set_color("black")
            autotext.set_fontsize(10)
            autotext.set_weight("bold")

        plt.title("Top Seller Share by Brazilian State", fontsize=12, fontweight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "04_sellers_by_state.png"), dpi=300)
        plt.close()

    @staticmethod
    def plot_revenue_share(df: pd.DataFrame):
        top_5 = df.head(5)
        others_revenue = df["total_revenue"].iloc[5:].sum()
        values = list(top_5["total_revenue"]) + [others_revenue]
        labels = list(top_5["category_name"]) + ["Others"]

        plt.figure(figsize=(7, 7))
        plt.pie(values, labels=labels, autopct="%1.1f%%", startangle=140)
        plt.title("Revenue Share Breakdown")
        plt.tight_layout()
        plt.savefig(os.path.join(PLOTS_DIR, "05_revenue_share.png"), dpi=300)
        plt.close()
