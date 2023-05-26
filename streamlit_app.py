import streamlit as st
import pandas as pd
import numpy as np
from st_pages import Page, show_pages
from helper_func import data_parser, styles, aiohttp_func
import asyncio
from streamlit_extras.no_default_selectbox import selectbox


# import cProfile
# import pstats
# import io
RELEVANT_COLS = [
    "product_id",
    "client_id",
    "product_category",
    "product_name",
    "active_ingredient",
    "manufacturer",
    "registration_type",
    "status",
    "country_origin",
    "applicant",
]


st.set_page_config(
    page_title="Product Registry",
    page_icon="🚨",
    initial_sidebar_state="expanded",
    layout="wide",
)

# styles.load_css_file("styles/main.css")
styles.local_css("styles.css")
styles.remote_css("https://fonts.googleapis.com/icon?family=Material+Icons")

show_pages(
    [
        Page("streamlit_app.py", "Product Indexing", "🕵️"),
        Page("st_pages/analyze.py", "Analytics", "📈"),
    ]
)

# asyncio.run(aiohttp_func.main_async_call())
data = data_parser.read_data("registered_products.parquet")
if st.experimental_user in ["test@localhost.com", "andrewsboateng137@gmail.com"]:
    if st.sidebar.button("Update Data", type="primary"):
        st.cache_data.clear()
        with st.spinner("Accessing FDA Database"):
            asyncio.run(aiohttp_func.main_async_call())


st.sidebar.header("Filter")
product_list = data["product_name"].unique().tolist()
product_list.sort()
st.sidebar.write("**Product Category**")

product_category = st.sidebar.multiselect(
    "prod_cat", options=data["product_category"].unique(), label_visibility="collapsed"
)
if product_category:
    data = data[data["product_category"].isin(product_category)]

st.sidebar.write("**Applicant**")
applicant_list = st.sidebar.multiselect(
    "applicant", options=data["applicant"].unique(), label_visibility="collapsed"
)
if applicant_list:
    data = data[data["applicant"].isin(applicant_list)]

st.sidebar.write("**Manufacturer**")
manufacturer_list = st.sidebar.multiselect(
    "manufacturer", options=data["manufacturer"].unique(), label_visibility="collapsed"
)
if manufacturer_list:
    data = data[data["manufacturer"].isin(manufacturer_list)]


st.title("Product Indexing")
st.write(
    "This is a product indexing tool. Search through over 40,000 registered products"
)


col1, col2 = st.columns([5, 1])
product_name = col1.text_input(
    "Search", placeholder="Search Product Name ...", label_visibility="collapsed"
)

button_clicked = col2.button("🔍", type="primary")

st.subheader("Registered Products Table")

if product_name:
    data = data[
        data["product_name"].str.contains(product_name, case=False, regex=False)
    ]

    data["Show Product Details"] = False
    RELEVANT_COLS.insert(0, "Show Product Details")
    main_data_holder = st.empty()
    checked_data_holder = st.empty()

    show_data = data[RELEVANT_COLS]
    checked_df = main_data_holder.experimental_data_editor(data[RELEVANT_COLS])

    if "checked_df" not in st.session_state:
        st.session_state["checked_df"] = True
    checked_df = checked_df[
        checked_df["Show Product Details"] == st.session_state["checked_df"]
    ]

    if checked_df.shape[0] == 1:
        main_data_holder.empty()
        unchecked_df = checked_data_holder.experimental_data_editor(checked_df)
        # st.write(unchecked_df["Show Product Details"].values[0])
        if unchecked_df["Show Product Details"].values[0] == False:
            st.session_state["checked_df"] = False
            st.experimental_rerun()
    else:
        checked_data_holder.empty()
        st.session_state["checked_df"] = True


else:
    st.dataframe(data[RELEVANT_COLS])
