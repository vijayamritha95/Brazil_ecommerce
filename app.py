import sys
import os
import pandas as pd
from flask import Flask, render_template

# Add project root to sys.path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from analysis.sqlqueries import SalesSQLQueries
from analysis.data_processing import DataProcessor

app = Flask(__name__)

# Initialize SQL Queries
sql_queries = SalesSQLQueries()

# Jinja Filters for formatting
@app.template_filter('format_currency')
def format_currency(value):
    try:
        return "${:,.2f}".format(float(value))
    except:
        return value

@app.template_filter('format_number')
def format_number(value):
    try:
        return "{:,}".format(int(value))
    except:
        return value

@app.template_filter('format_percent')
def format_percent(value):
    try:
        return "{:.2f}%".format(float(value))
    except:
        return value

@app.route('/')
def dashboard():
    # Fetch and process category data
    df_categories = sql_queries.query_joins_aggregates_groupby_having()
    df_categories_clean = DataProcessor.clean_category_sales(df_categories)
    
    # Calculate KPIs
    total_revenue = float(df_categories_clean['total_revenue'].sum())
    total_orders = int(df_categories_clean['total_orders'].sum())
    product_categories = int(len(df_categories_clean))
    avg_order_value = float(total_revenue / total_orders) if total_orders > 0 else 0
    
    # Top 10 categories for charts
    top_categories = df_categories_clean.head(10).to_dict('records')
    all_categories = df_categories_clean.to_dict('records')
    
    return render_template('dashboard.html', 
                           total_revenue=total_revenue,
                           total_orders=total_orders,
                           product_categories=product_categories,
                           avg_order_value=avg_order_value,
                           top_categories=top_categories,
                           all_categories=all_categories)

@app.route('/sql/order-freight')
def order_freight():
    df_freight = sql_queries.query_select_where_orderby()
    orders = df_freight.to_dict('records')
    
    sql_query = """
    SELECT order_id, product_id, price, freight_value 
    FROM order_items
    WHERE freight_value > 50.00
    ORDER BY price DESC
    LIMIT 10;
    """
    return render_template('order_freight.html', orders=orders, sql_query=sql_query)

@app.route('/sql/category-sales')
def category_sales():
    df_categories = sql_queries.query_joins_aggregates_groupby_having()
    df_categories_clean = DataProcessor.clean_category_sales(df_categories)
    categories = df_categories_clean.to_dict('records')
    
    sql_query = """
    SELECT COALESCE(t.product_category_name_english, 'Uncategorized') AS category_name,
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
    return render_template('category_sales.html', categories=categories, sql_query=sql_query)

@app.route('/sql/seller-performance')
def seller_performance():
    df_sellers = sql_queries.query_cte_and_window_functions()
    df_sellers_clean = DataProcessor.process_seller_rankings(df_sellers)
    sellers = df_sellers_clean.to_dict('records')
    
    sql_query = """
    WITH SellerMetrics AS (
        SELECT s.seller_id, s.seller_state, COUNT(DISTINCT i.order_id) AS total_orders, SUM(i.price) AS total_revenue
        FROM sellers s
        JOIN order_items i ON s.seller_id = i.seller_id
        JOIN orders o ON i.order_id = o.order_id
        WHERE o.order_status = 'delivered'
        GROUP BY s.seller_id, s.seller_state
    ),
    RankedSellers AS (
        SELECT seller_id, seller_state, total_revenue,
               ROW_NUMBER() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS seller_row_num,
               RANK() OVER (PARTITION BY seller_state ORDER BY total_revenue DESC) AS state_rank,
               DENSE_RANK() OVER (ORDER BY total_revenue DESC) AS global_revenue_dense_rank
        FROM SellerMetrics
    )
    SELECT * FROM RankedSellers
    WHERE state_rank <= 3
    ORDER BY seller_state, state_rank;
    """
    return render_template('seller_performance.html', sellers=sellers, sql_query=sql_query)

if __name__ == '__main__':
    app.run(debug=True, port=5000)