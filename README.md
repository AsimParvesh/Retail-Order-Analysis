# 🛍️ Retail Order Analysis Dashboard

An interactive data analysis application built using **Streamlit** and **MySQL (TiDB Cloud)** to explore and visualize retail order data. This tool supports business intelligence through pre-defined SQL insights powered by a real-time database connection.

---

## 📌 Overview

This project allows users to:
- Analyze single-table and multi-table insights from a retail order dataset.
- Execute 20+ pre-written SQL queries grouped by business context.
- Visualize results dynamically with bar charts, line graphs, and interactive tables.
- Connect directly to a **TiDB Cloud** MySQL-compatible database.

---

## 🚀 Features

✅ **Live Database Connectivity** (TiDB Cloud)  
✅ **SQL-Based Querying** (20+ pre-defined queries)  
✅ **Data Visualization** using tables, bar charts, and line graphs  
✅ **Sidebar Controls** for selecting query type and viewing SQL code  
✅ **Dynamic Table Creation & Data Migration** (only runs once)

---

## 💡 Business Insights Covered

### 📋 Single Table Queries
- Top Revenue-Generating Products
- Most Discounted Categories
- Average Sale & Cost Price by Category
- Most Frequently Ordered Products
- Price Extremes (Cheapest / Most Expensive Products)
- Profit Analysis by Category

### 🔄 Multi Table Queries
- Profit Margin by City
- Revenue by Year & Month
- Most Popular Shipping Mode
- Discount Trends by Region
- Segment-based Order Volume
- Regional Revenue Leaders

---

## 🖼️ Sample Visuals

> *Visualizations include line charts for trends and bar charts for comparisons.*

- 📊 **Bar Charts**: Category-based comparisons (e.g. discount, revenue, frequency)
- 📈 **Line Charts**: Yearly and monthly revenue trends

---

## 🧰 Tech Stack

| Tool        | Purpose                             |
|-------------|-------------------------------------|
| **Python**  | Core programming language           |
| **Streamlit** | Web app interface for data querying |
| **MySQL / TiDB Cloud** | Backend database for storage and querying |
| **pandas**  | DataFrame handling                  |
| **MySQL Connector** | Connect Streamlit to TiDB Cloud |

---

## 🛠️ Setup Instructions

🔧 1. Clone the Repository

git clone https://github.com/your-username/retail-order-analysis.git
cd retail-order-analysis


📦 2. Install Dependencies

pip install -r requirements.txt


🚀 3. Launch the App

streamlit run RetailOrder_AnalysisProject.py


🌐 4. Replace Credentials
Make sure you update the following in the get_connection() function:

host

user

password

database


🗃️ Project Structure

retail-order-analysis/
│
├── RetailOrder_AnalysisProject.py     # Streamlit app code
├── requirements.txt                   # Python dependencies
└── README.md                          # Project documentation


📌 Notes
Tables (Orders, Order_Items) are auto-created if they don’t exist.

Data is inserted only once from the master table OrderData during first-time setup.

Queries are pre-loaded and categorized into Single Table and Multi Table queries.

Chart display is automated based on the nature of the query.



👨‍💻 Author
Asim Parvesh
Data Enthusiast | Python Developer | BI Analyst

📜 License
This project is open-source and available under the MIT License.


> ✅ **Tips**:
- Replace `your-username` and `your-profile` with your actual GitHub and LinkedIn links.
- Add a `screenshots/` folder if you want to include a visual preview of your dashboard.
- Push `requirements.txt` with:
