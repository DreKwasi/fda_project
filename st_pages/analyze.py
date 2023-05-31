import streamlit as st
import pandas as pd
from helper_func import data_parser, styles, metrics, charts, st_filters, utils
from streamlit_extras.metric_cards import style_metric_cards

# import cProfile
# import pstats
# import io


st.set_page_config(
    page_title="Health Watch",
    page_icon="🛍️",
    initial_sidebar_state="expanded",
    layout="wide",
)

styles.local_css("styles/main.css")

data = data_parser.read_data("registered_products.parquet")
download_data_btn = st.sidebar.empty()

st.sidebar.header("Filters", anchor=False)
filters = st_filters.filter_widgets(data)
data = st_filters.filter_data(data.copy(), *filters)



st.header("General Insights")

col1, col2 = st.columns(2)

col1.metric("**Total Registrations**", value=metrics.number_of_registrations(data))
col2.metric("**Number of Renewals**", value=metrics.number_of_renewals(data))

col1.metric("**Number of Unique Products**", value=metrics.number_of_products(data))
col2.metric("**Number of Unique Applicants**", value=metrics.number_of_applicants(data))
style_metric_cards()

st.subheader("Data View")
with st.expander("**Click to Show Data**"):
    download_data = utils.convert_df(data)
    st.download_button(
        "Download Full Data",
        data=download_data,
        file_name="reg_by_category.csv",
        mime="text/csv",
        key="main_data_download",
        help="Data is Affected By Filters",
    )
    st.dataframe(data)

st.subheader("Products Breakdown")
# Registration Trend
freq_dict = {"Month": "MS", "Quarter": "QS", "Year": "AS"}
freq = st.selectbox("Select Date Frequency", options=["Month", "Quarter", "Year"])
registration_trend = (
    data.groupby(by=[pd.Grouper(key="registration_date", freq=freq_dict[freq])])
    .agg(number_of_registrations=("product_id", "count"))
    .reset_index()
)
st.write("<h5> <u> Trend of Registrations by Date </u> </h5>", unsafe_allow_html=True)
charts.trend_chart(registration_trend, freq)

st.write("<h5> <u> Grouped Registrations by Category </u> </h5>", unsafe_allow_html=True)
charts.grouped_chart(data, "product_category")

st.subheader("Clients Breakdown")
st.write("<h5> <u> Grouped Registrations by Applicants </u> </h5>", unsafe_allow_html=True)
charts.grouped_chart(data, "applicant")
