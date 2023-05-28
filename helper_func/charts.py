import plotly_express as px
import pandas as pd
import streamlit as st


def trend_chart(data):
    fig = px.bar(data, x="registration_date", y="number_of_registrations")
    st.plotly_chart(fig, use_container_width=True)

def grouped_chart(data):
    fig = px.bar(data, x="product_category", y="number_of_registrations", color="product_category")
    st.plotly_chart(fig, use_container_width=True)