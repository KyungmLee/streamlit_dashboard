import pandas as pd
import streamlit as st
from sqlalchemy import text
from db.connection import get_engine

########################################################
# customer table CRUD functions
########################################################

@st.cache_data(ttl=300)
def get_all_customers():
    engine = get_engine()
    sql = "SELECT * FROM customers ORDER BY id DESC"
    return pd.read_sql(sql, engine)

@st.cache_data(ttl=300)
def get_filtered_customers(name_keyword: str, region: str):
    engine = get_engine()

    sql = """
    SELECT *
    FROM customers
    WHERE (:name_keyword = '' OR name LIKE :name_pattern)
      AND (:region = '전체' OR region = :region)
    ORDER BY id DESC
    """

    params = {
        "name_keyword": name_keyword,
        "name_pattern": f"%{name_keyword}%",
        "region": region
    }

    return pd.read_sql(text(sql), engine, params=params)

@st.cache_data(ttl=300)
def get_summary():
    engine = get_engine()

    sql = """
    SELECT
        COUNT(*) AS customer_count,
        ROUND(AVG(age), 1) AS avg_age,
        ROUND(SUM(sales), 2) AS total_sales,
        ROUND(AVG(sales), 2) AS avg_sales
    FROM customers
    """
    return pd.read_sql(sql, engine)

@st.cache_data(ttl=300)
def get_region_summary():
    engine = get_engine()

    sql = """
    SELECT region, COUNT(*) AS customer_count, SUM(sales) AS total_sales
    FROM customers
    GROUP BY region
    ORDER BY total_sales DESC
    """
    return pd.read_sql(sql, engine)

def insert_customer(name, region, age, join_date, sales):
    engine = get_engine()
    sql = """
    INSERT INTO customers (name, region, age, join_date, sales)
    VALUES (:name, :region, :age, :join_date, :sales)
    """
    with engine.begin() as conn:
        conn.execute(text(sql), {
            "name": name,
            "region": region,
            "age": age,
            "join_date": join_date,
            "sales": sales
        })
    clear_data_cache()

def update_customer(customer_id, name, region, age, join_date, sales):
    engine = get_engine()
    sql = """
    UPDATE customers
    SET name=:name, region=:region, age=:age, join_date=:join_date, sales=:sales
    WHERE id=:customer_id
    """
    with engine.begin() as conn:
        conn.execute(text(sql), {
            "customer_id": customer_id,
            "name": name,
            "region": region,
            "age": age,
            "join_date": join_date,
            "sales": sales
        })
    clear_data_cache()

def delete_customer(customer_id):
    engine = get_engine()
    sql = "DELETE FROM customers WHERE id=:customer_id"
    with engine.begin() as conn:
        conn.execute(text(sql), {"customer_id": customer_id})
    clear_data_cache()

def clear_data_cache():
    st.cache_data.clear()


#######################################################
# sale table CRUD functions
#######################################################

def get_all_sales():
    engine = get_engine()
    query = """
        SELECT id, order_date, product_name, category, quantity, price, region, created_at
        FROM sales
        ORDER BY id DESC
    """
    return pd.read_sql(query, engine)

def search_sales(category=None, region=None, keyword=None):
    engine = get_engine()

    conditions = []
    params = {}

    base_query = """
        SELECT id, order_date, product_name, category, quantity, price, region, created_at
        FROM sales
        WHERE 1=1
    """

    if category:
        conditions.append("AND category = :category")
        params["category"] = category

    if region:
        conditions.append("AND region = :region")
        params["region"] = region

    if keyword:
        conditions.append("AND product_name LIKE :keyword")
        params["keyword"] = f"%{keyword}%"

    final_query = base_query + "\n".join(conditions) + "\nORDER BY id DESC"

    return pd.read_sql(text(final_query), engine, params=params)

def insert_sale(order_date, product_name, category, quantity, price, region):
    engine = get_engine()
    query = text("""
        INSERT INTO sales (order_date, product_name, category, quantity, price, region)
        VALUES (:order_date, :product_name, :category, :quantity, :price, :region)
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            "order_date": order_date,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "region": region
        })

def update_sale(sale_id, order_date, product_name, category, quantity, price, region):
    engine = get_engine()
    query = text("""
        UPDATE sales
        SET order_date = :order_date,
            product_name = :product_name,
            category = :category,
            quantity = :quantity,
            price = :price,
            region = :region
        WHERE id = :sale_id
    """)
    with engine.begin() as conn:
        conn.execute(query, {
            "sale_id": sale_id,
            "order_date": order_date,
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "price": price,
            "region": region
        })

def delete_sale(sale_id):
    engine = get_engine()
    query = text("DELETE FROM sales WHERE id = :sale_id")
    with engine.begin() as conn:
        conn.execute(query, {"sale_id": sale_id})

def get_sale_by_id(sale_id):
    engine = get_engine()
    query = text("""
        SELECT id, order_date, product_name, category, quantity, price, region
        FROM sales
        WHERE id = :sale_id
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"sale_id": sale_id}).mappings().first()
        return dict(result) if result else None