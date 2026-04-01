import streamlit as st
import pandas as pd

# 원격DB 접속을 위해 cryptography 설치 필요
# pip install cryptography

st.header("AWS RDS MySQL 접속 예제")
st.markdown("dashboard_db의 customers 데이터를 조회하여 표시하기")
conn = st.connection('dashboard_db', type='sql')

df = conn.query("SELECT * FROM customers LIMIT 100", ttl=300)
st.dataframe(df)
