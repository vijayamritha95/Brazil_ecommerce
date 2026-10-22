import pandas as pd
from sqlalchemy import text
from database.connection import get_engine, logger


class SalesSQLQueries:
    def __init__(self):
        self.engine = get_engine()

    def query_select_where_orderby(self) -> pd.DataFrame:
        """
        1. SELECT, WHERE, ORDER BY
        Fetches delivered orders with freight value > $50, ordered by price.
        """
        query = """
        SELECT 
            order_id, 
            product_id, 
            price, 
            freight_value 
        FROM order_items
        WHERE freight_value > 50.00
        ORDER BY price DESC
        LIMIT 10;
        """
        return pd.read_sql_query(text(query), self.engine)

    def query_joins_aggregates_groupby_having(self) -> pd.DataFrame:
        """
        2. JOIN, GROUP BY, HAVING, Aggregate Functions (SUM, COUNT, AVG)
        Calculates total revenue and order metrics by product category.
        """
        query = """
        SELECT 
            COALESCE(t.product_category_name_english, 'Uncategorized') AS category_name,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(i.price) AS total_revenue,
            ROUND(AVG(i.price)::numeric, 2) AS average_order_value
        FROM orders o
        JOIN order_items i ON o.order_id = i.order_id
        JOIN products p ON i.product_id = p.product_id
        LEFT JOIN category_name_translation t ON p.product_category_name = t.product_category_name
        WHERE o.order_status = 'delivered'
        GROUP BY category_name
        HAVING SUM(i.price) > 10000
        ORDER BY total_revenue DESC;
        """
        return pd.read_sql_query(text(query), self.engine)

    def query_subquery(self) -> pd.DataFrame:
        """
        3. Subqueries
        Finds customers whose total spend is higher than the average total spend per customer.
        """
        query = """
        SELECT 
            customer_unique_id,
            total_spent
        FROM (
            SELECT 
                c.customer_unique_id,
                SUM(p.payment_value) AS total_spent
            FROM customers c
            JOIN orders o ON c.customer_id = o.customer_id
            JOIN order_payments p ON o.order_id = p.order_id
            WHERE o.order_status = 'delivered'
            GROUP BY c.customer_unique_id
        ) AS customer_spending
        WHERE total_spent > (
            SELECT AVG(user_total)
            FROM (
                SELECT SUM(payment_value) AS user_total
                FROM orders o2
                JOIN order_payments p2 ON o2.order_id = p2.order_id
                WHERE o2.order_status = 'delivered'
                GROUP BY o2.customer_id
            ) AS avg_table
        )
        ORDER BY total_spent DESC
        LIMIT 10;
        """
        return pd.read_sql_query(text(query), self.engine)

    def query_cte_and_window_functions(self) -> pd.DataFrame:
        """
        4. CTEs & Window Functions (ROW_NUMBER, RANK, DENSE_RANK)
        Ranks sellers within each Brazilian state based on revenue.
        """
        query = """
        WITH SellerMetrics AS (
            SELECT 
                s.seller_id,
                s.seller_state,
                COUNT(DISTINCT i.order_id) AS total_orders,
                SUM(i.price) AS total_revenue
            FROM sellers s
            JOIN order_items i ON s.seller_id = i.seller_id
            JOIN orders o ON i.order_id = o.order_id
            WHERE o.order_status = 'delivered'
            GROUP BY s.seller_id, s.seller_state
        ),
        RankedSellers AS (
            SELECT 
                seller_id,
                seller_state,
                total_revenue,
                ROW_NUMBER() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS seller_row_num,
                RANK() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS state_rank,
                DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS global_revenue_dense_rank
            FROM SellerMetrics
        )
        SELECT * 
        FROM RankedSellers
        WHERE state_rank <= 3
        ORDER BY seller_state, state_rank;
        """
        return pd.read_sql_query(text(query), self.engine)
