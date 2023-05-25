import streamlit as st
import pandas as pd
import numpy as np
from st_pages import Page, show_pages
from helper_func import data_parser, styles, aiohttp_func
import asyncio

# from streamlit_extras.app_logo import add_logo
# import cProfile
# import pstats
# import io
RELEVANT_COLS = [
    "product_id",
    "client_id",
    "product_category",
    "product_sub_category",
    "registration_number",
    "product_name",
    "generic_name",
    "strength",
    "active_ingredient",
    "representative_company_local_agent_applicant",
    "manufacturer",
    "registration_type",
    "status",
    "country_origin",
    "region",
    "applicant",
    "registerd_importers",
    "client_name",
    "postal_address",
    "sim_contact",
    "telephone_number",
    "email",
]


st.set_page_config(
    page_title="Market Registry",
    page_icon="🏦",
    initial_sidebar_state="expanded",
    layout="wide",
)

# styles.load_css_file("styles/main.css")
styles.local_css("styles.css")
styles.remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")

show_pages(
    [
        Page("streamlit_app.py", "Home", "🏪"),
        Page("st_pages/analyze.py", "Analytics", "💳"),
        Page("st_pages/search.py", "Product Indexing", "📈"),
    ]
)

# asyncio.run(aiohttp_func.main_async_call())
data = data_parser.read_data("registered_products.parquet")

if st.sidebar.button("Update Data", type="primary"):
    st.cache_data.clear()
    with st.spinner("Accessing FDA Database"):
        asyncio.run(aiohttp_func.main_async_call())


st.sidebar.header("Filter")

st.sidebar.write("Select A Product Category")

product_category = st.sidebar.multiselect(
    "prod_cat", options=data["product_category"].unique(), label_visibility="collapsed"
)
if product_category:
    data = data[data["product_category"].isin(product_category)]

st.sidebar.write("Select A Product Sub Category")
product_sub_category = st.sidebar.multiselect(
    "prod_sub_cat",
    options=data["product_sub_category"].unique(),
    label_visibility="collapsed",
)
if product_sub_category:
    data = data[data["product_sub_category"].isin(product_sub_category)]

st.sidebar.write("Select a Manufacturer")
manufacturer = st.sidebar.multiselect(
    "manufacturer", options=data["manufacturer"].unique(), label_visibility="collapsed"
)
if manufacturer:
    data = data[data["manufacturer"].isin(manufacturer)]


st.title("Product Indexing")
st.write(
    "This is a product indexing tool. Search through over 40,000 registered products"
)


col1, col2 = st.columns([3, 1])
product_name = col1.text_input(
    "Search", placeholder="Search Product Name ... ", label_visibility="collapsed"
)
button_clicked = col2.button("🔍", type="primary")


data = data[data["product_name"].str.contains(product_name, case=False)]
st.dataframe(data[RELEVANT_COLS])