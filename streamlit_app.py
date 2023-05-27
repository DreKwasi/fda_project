import streamlit as st
import pandas as pd
import numpy as np
from st_pages import Page, show_pages
from helper_func import data_parser, styles, aiohttp_func, forms, utils
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
    page_icon="🛍️",
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


data = data_parser.read_data("registered_products.parquet")
if st.experimental_user.email in ["test@localhost.com", "andrewsboateng137@gmail.com"]:
    if st.sidebar.button("Update Data", type="primary"):
        st.cache_data.clear()
        with st.spinner("Accessing FDA Database"):
            asyncio.run(aiohttp_func.main_async_call())


query_params = st.experimental_get_query_params()

product_index = "all_products"
if query_params:
    try:
        product_index = query_params["product_index"][0]
    except ValueError:
        pass


def product_list_view(data):
    st.sidebar.header("Filter")
    
    st.sidebar.write("**Select Number of Entries**")
    num = st.sidebar.slider("number_of_entries", min_value=5, max_value=100, value=10, label_visibility="collapsed", step=10)
    
    product_list = data["product_name"].unique().tolist()
    product_list.sort()
    st.sidebar.write("**Product Category**")

    product_category = st.sidebar.multiselect(
        "prod_cat",
        options=data["product_category"].unique(),
        label_visibility="collapsed",
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
        "manufacturer",
        options=data["manufacturer"].unique(),
        label_visibility="collapsed",
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
    col2.button("🔍", type="primary")

    st.subheader("Registered Products Table", anchor=None)

    if product_name:
        filtered_data = data[
            data["product_name"].str.contains(product_name, case=False, regex=False)
        ].copy()
        st.info(f"{filtered_data.shape[0]} Products Found")

        filtered_data = filtered_data.assign(Show_Product_Details=False)
        start_index, end_index = utils.pagination(filtered_data, num)
        filtered_data = filtered_data.iloc[start_index:end_index, :]
        RELEVANT_COLS.insert(0, "Show_Product_Details")
        main_data_holder = st.empty()

        checked_df = main_data_holder.experimental_data_editor(
            filtered_data[RELEVANT_COLS],
            key="df_edit",
        )
        product_row = checked_df[checked_df["Show_Product_Details"] == True]
        if not product_row.empty:
            st.experimental_set_query_params(product_index=product_row.index[0])
            st.experimental_rerun()

    else:
        start_index, end_index = utils.pagination(data, num)
        data = data.iloc[start_index:end_index, :]
        st.dataframe(data[RELEVANT_COLS])


if product_index == "all_products":
    product_list_view(data)
else:
    forms.detailed_view(data, product_index)
