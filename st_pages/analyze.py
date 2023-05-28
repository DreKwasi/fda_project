import streamlit as st
import pandas as pd
import numpy as np
from helper_func import data_parser, styles, metrics, charts, utils
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
col1.metric("Number of Unique Products", value=metrics.number_of_products(data))
col2.metric("Number of Unique Applicants", value=metrics.number_of_applicants(data))
col1.metric("Total Registrations", value=metrics.number_of_registrations(data))
col2.metric("Number of Renewals", value=metrics.number_of_renewals(data))
style_metric_cards()

st.subheader("Products Breakdown")
# Registration Trend
registration_trend = (
    data.groupby(by=[pd.Grouper(key="registration_date", freq="MS")])
    .agg(number_of_registrations=("product_id", "count"))
    .reset_index()
)
charts.trend_chart(registration_trend)

category_grouped = (
    data.groupby(by=["product_category"])
    .agg(number_of_registrations=("product_id", "count"))
    .reset_index()
)
charts.grouped_chart(category_grouped)

st.subheader("Clients Breakdown")
