import streamlit as st
import pandas as pd
import numpy as np
from helper_func import data_parser, styles, aiohttp_func, forms, utils
import asyncio
from streamlit_extras.metric_cards import style_metric_cards

# import cProfile
# import pstats
# import io


st.set_page_config(
    page_title="Product Registry",
    page_icon="🛍️",
    initial_sidebar_state="expanded",
    layout="wide",
)

styles.local_css("styles/main.css")

data = data_parser.read_data("registered_products.parquet")

st.header("General Insights")

col1, col2 = st.columns(2)
col1.metric("Number of Products", value=data.shape[0])
col2.metric("Number of Applicants", value=data.shape[0])
col1.metric("Number of New Registrations", value=data.shape[0])
col2.metric("Number of Renewals", value=data.shape[0])
style_metric_cards()

st.subheader("Products Breakdown")
st.subheader("Clients Breakdown")
