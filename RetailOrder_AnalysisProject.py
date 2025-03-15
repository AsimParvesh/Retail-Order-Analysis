import mysql.connector
import streamlit as st
import pandas as pd

## ---> I have defined the connection string here, so that i can call it in future
def get_connection():
    
    return mysql.connector.connect(
  host = "gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
  port = 4000,
  user = "daLWWT7xQQreKGi.root",
  password = "PnDmBc7huh9RKVfz",
  database = "Retail_Analysis"
)


## ---> Here I have set up the Database to query data from it and perform insight
def setup_database():
    connection = get_connection()
    cursor = connection.cursor()

    # Create tables if they don't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INT PRIMARY KEY,
            order_date DATE,
            ship_mode VARCHAR(50),
            segment VARCHAR(50),
            country VARCHAR(100),
            city VARCHAR(100),
            state VARCHAR(100),
            postal_code VARCHAR(20),
            region VARCHAR(50)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Order_Items (
            order_item_id INT PRIMARY KEY AUTO_INCREMENT,
            order_id INT,
            product_id VARCHAR(50),
            category VARCHAR(50),
            sub_category VARCHAR(50),
            cost_price DECIMAL(10,2),
            list_price DECIMAL(10,2),
            quantity INT,
            discount_percent DECIMAL(5,2),
            FOREIGN KEY (order_id) REFERENCES Orders(order_id)
        )
    """)

    # Check if data is already migrated (Runs only if tables are empty)
    cursor.execute("SELECT COUNT(*) FROM Orders")
    orders_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Order_Items")
    items_count = cursor.fetchone()[0]

    if orders_count == 0 and items_count == 0:  # Only migrate if both tables are empty
        cursor.execute("""
            INSERT INTO Orders (order_id, order_date, ship_mode, segment, country, city, state, postal_code, region)
            SELECT DISTINCT order_id, order_date, ship_mode, segment, country, city, state, postal_code, region
            FROM Retail_Analysis.OrderData;
        """)

        cursor.execute("""
            INSERT INTO Order_Items (order_id, product_id, category, sub_category, cost_price, list_price, quantity, discount_percent)
            SELECT order_id, product_id, category, sub_category, cost_price, list_price, quantity, discount_percent
            FROM Retail_Analysis.OrderData;
        """)

        st.success("Tables created and data migrated successfully!")

    connection.commit()
    cursor.close()
    connection.close()




## ---> Function to fetch data from tables
def fetch_data(table_name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 10")
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    connection.close()
    return columns, rows

## ---> Function to execute a query
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return columns, rows



## ---> Automatically run setup in the background (only once)
setup_database()



# --- Queries Stored as Named Variables ---

#Single-Given
top_10_revenue="SELECT product_id, category, sub_category, (list_price - discount_percent) * quantity AS Revenue FROM order_items ORDER BY Revenue DESC LIMIT 10"

#Single-Given
total_discount_per_category = """
SELECT 
    category, 
    ROUND(SUM((list_price * discount_percent / 100) * quantity), 2) AS total_discount
FROM order_items
GROUP BY category
ORDER BY total_discount DESC;
"""

#Single-Given
average_sale_price= """
SELECT 
    sub_category, 
    ROUND(SUM((list_price - (list_price * discount_percent / 100)) * quantity) / SUM(quantity), 2) AS 'Average Sale Price'
FROM Retail_Analysis.`Order_Items`
GROUP BY sub_category;"""

#Single-Given
total_profit_per_category="""
SELECT category, 
       SUM((list_price - cost_price) * quantity) AS Total_Profit
FROM Order_Items
GROUP BY category;
"""

#Single-Given
product_catogory_with_highest_total_profit="""
SELECT category, 
       SUM((list_price - cost_price) * quantity) AS Total_Profit
FROM Order_Items
GROUP BY category
ORDER BY Total_Profit DESC
LIMIT 1;
"""

#Single-Own
most_discounted_product_catogory="""
SELECT category, 
       ROUND(SUM(list_price * discount_percent / 100 * quantity), 2) AS Total_Discount
FROM Order_Items
GROUP BY category
ORDER BY Total_Discount DESC
LIMIT 1;
"""

#Single-Own
most_frequently_ordered_sub_Category="""
SELECT sub_category, 
       SUM(quantity) AS Total_Quantity
FROM Order_Items
GROUP BY sub_category
ORDER BY Total_Quantity DESC
LIMIT 1;
"""

#Single-Own
average_cost_price_per_category="""
SELECT category, 
       ROUND(AVG(cost_price), 2) AS Avg_Cost_Price
FROM Order_Items
GROUP BY category;
"""

#Single-Own
cheapest_product_per_category="""
SELECT category, 
       MIN(list_price) AS Min_Price
FROM Order_Items
GROUP BY category;
"""

#Single-Own
most_expensive_product_sold="""
SELECT product_id, category, sub_category, 
       list_price AS Highest_Price
FROM Order_Items
ORDER BY list_price DESC
LIMIT 1;
"""

#--------------------------------------------------------------------------------------------------------------------------------------#

#Multi-Given
top_5_cities_profit_margin = """
SELECT 
    o.city, 
    ROUND(SUM((oi.list_price - oi.cost_price) * oi.quantity) / SUM((oi.list_price - oi.discount_percent) * oi.quantity) * 100, 2) AS profit_margin 
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id 
GROUP BY o.city
HAVING SUM((oi.list_price - oi.discount_percent) * oi.quantity) > 0
ORDER BY profit_margin DESC 
LIMIT 5;
"""

#Multi-Given
highest_average_sale_region = """
        SELECT o.region, 
               ROUND(SUM((oi.list_price - (oi.list_price * oi.discount_percent / 100)) * oi.quantity) / SUM(oi.quantity), 2) 
               AS avg_sale_price
        FROM Order_Items oi 
        JOIN Orders o ON oi.order_id = o.order_id
        GROUP BY o.region
        ORDER BY avg_sale_price DESC
        LIMIT 1;
    """

#Multi-Given
top_3_segment_with_highest_orders="""
SELECT o.segment, 
       SUM(oi.quantity) AS Total_Quantity
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.segment
ORDER BY Total_Quantity DESC
LIMIT 3;
"""

#Multi-Given
average_discount_percentage_per_region="""
SELECT o.region, 
       ROUND(AVG(oi.discount_percent), 2) AS Avg_Discount_Percentage
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.region;
"""

#Multi-Given
total_revenue_generated_per_year="""
SELECT YEAR(o.order_date) AS Year, 
       ROUND(SUM((oi.list_price - (oi.list_price * oi.discount_percent / 100)) * oi.quantity), 2) AS Total_Revenue
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY Year
ORDER BY Year;
"""

#Multi-Own
highest_total_revenue_month="""
SELECT DATE_FORMAT(o.order_date, '%Y-%m') AS Order_Month, 
       ROUND(SUM((oi.list_price - (oi.list_price * oi.discount_percent / 100)) * oi.quantity), 2) AS Total_Revenue
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY Order_Month
ORDER BY Total_Revenue DESC
LIMIT 1;
"""

#Multi-Own
most_popular_ship_mode="""
SELECT o.ship_mode, 
       COUNT(o.order_id) AS Order_Count
FROM Orders o
GROUP BY o.ship_mode
ORDER BY Order_Count DESC
LIMIT 1;
"""

#Multi-Own
most_profitable_state="""
SELECT o.state, 
       SUM((oi.list_price - oi.cost_price) * oi.quantity) AS Total_Profit
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.state
ORDER BY Total_Profit DESC
LIMIT 1;
"""

#Multi-Own
category_with_the_highest_revenue_in_each_region="""
SELECT o.region, oi.category, 
       ROUND(SUM((oi.list_price - (oi.list_price * oi.discount_percent / 100)) * oi.quantity), 2) AS Total_Revenue
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.region, oi.category
ORDER BY o.region, Total_Revenue DESC;
"""

#Multi-Own
region_with_the_lowest_average_discount_given="""
SELECT o.region, 
       ROUND(AVG(oi.discount_percent), 2) AS Avg_Discount_Percentage
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.region
ORDER BY Avg_Discount_Percentage ASC
LIMIT 1;
"""



## ---> Streamlit UI
st.title("Retail Order Analysis")


# Sidebar Selection
st.sidebar.subheader("Choose Query Type")
query_type = st.sidebar.radio("Query Category", ["Single Table Queries", "Multi Table Queries"])



# --- Single Table Queries ---
single_queries = {
    "Top 10 Revenue": top_10_revenue,
    "Total Discount Per Category": total_discount_per_category,
    "Average Sale Price": average_sale_price,
    "Total Profit Per Category": total_profit_per_category,
    "Product Category With Highest Total Profit": product_catogory_with_highest_total_profit,
    "Most Discounted Product Category": most_discounted_product_catogory,
    "Most Frequently Ordered Sub Category": most_frequently_ordered_sub_Category,
    "Average Cost Price Per Category": average_cost_price_per_category,
    "Cheapest Product Per Category": cheapest_product_per_category,
    "Most Expensive Product Sold": most_expensive_product_sold
}

# --- Multi Table Queries ---
multi_queries = {
    "Top 5 Cities Profit Margin": top_5_cities_profit_margin,
    "Highest Average Sale Region": highest_average_sale_region,
    "Top 3 Segments With Highest Orders": top_3_segment_with_highest_orders,
    "Average Discount Percentage Per Region": average_discount_percentage_per_region,
    "Total Revenue Generated Per Year": total_revenue_generated_per_year,
    "Highest Total Revenue Month": highest_total_revenue_month,
    "Most Popular Ship Mode": most_popular_ship_mode,
    "Most Profitable State": most_profitable_state,
    "Category With The Highest Revenue In Each Region": category_with_the_highest_revenue_in_each_region,
    "Region With The Lowest Average Discount Given": region_with_the_lowest_average_discount_given
}



# --- Selecting Queries ---
if query_type == "Single Table Queries":
    selected_query_name = st.sidebar.selectbox("Select a Query", list(single_queries.keys()))
    selected_query = single_queries[selected_query_name]
else:
    selected_query_name = st.sidebar.selectbox("Select a Query", list(multi_queries.keys()))
    selected_query = multi_queries[selected_query_name]

# --- Run Query ---
cols, data = run_query(selected_query)

# --- Convert to DataFrame ---
df = pd.DataFrame(data, columns=cols)
df.reset_index(drop=True, inplace=True)

# --- Display Table ---
st.write(f"### {selected_query_name}")
st.table(df)

# --- Visualization Logic ---
# Bar Charts (for category-based comparisons)
bar_chart_queries = [
    "Total Discount Per Category",
    "Total Profit Per Category",
    "Product Category With Highest Total Profit",
    "Most Discounted Product Category",
    "Most Frequently Ordered Sub Category",
    "Average Cost Price Per Category",
    "Cheapest Product Per Category",
    "Top 5 Cities Profit Margin",
    "Top 3 Segments With Highest Orders",
    "Average Discount Percentage Per Region",
    "Most Profitable State",
    "Category With The Highest Revenue In Each Region"
]

# Line Charts (for time-based trends)
line_chart_queries = [
    "Total Revenue Generated Per Year",
    "Highest Total Revenue Month"
]

# Display Bar Chart
if selected_query_name in bar_chart_queries:
    st.bar_chart(df.set_index(cols[0]))

# Display Line Chart
elif selected_query_name in line_chart_queries:
    st.line_chart(df.set_index(cols[0]))

# --- Sidebar Display for Query ---
st.sidebar.subheader("Executed Query")
st.sidebar.code(selected_query, language="sql")