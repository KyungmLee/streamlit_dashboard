# 페이지가 바뀌어도 유지되는 검색조건, 페이지 번호, 페이지 사이즈 등을 session_state로 관리
import streamlit as st

def init_session_state():
    defaults = {
        "search_name": "",
        "search_region": "전체",
        "page_number": 1,
        "page_size": 10,
        "selected_customer_id": None,
        "dashboard_refresh_count": 0,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value