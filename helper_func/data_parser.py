import numpy as np
import streamlit as st
from .firestore_func import download_blob
from streamlit_lottie import st_lottie_spinner
from helper_func import utils

# import time


def read_data(filename):
    # start = time.perf_counter()
    with st.spinner("Accessing Cloud Database ..."):
        with st_lottie_spinner(
            utils.load_lottiefile("assets/animations/data_transfer.json"), height=500
        ):
            df = download_blob(f"data/{filename}", f"assets/{filename}")
    # end = time.perf_counter()
    # print(f"Download Time: {end - start}")

    data = clean_data(df)
    # data.to_csv("data.csv", index=False)

    return data


@st.cache_data(show_spinner=False)
def clean_data(df):
    string_cols = [
        "product_category",
        "product_sub_category",
        "manufacturer",
        "product_name",
        "generic_name",
        "active_ingredient",
        "representative_company_local_agent_applicant",
        "applicant",
        "client_name",
    ]
    data = df.copy()

    data[string_cols] = (
        data[string_cols].fillna("Not Specified").apply(lambda x: x.str.title())
    )
    data[string_cols] = data[string_cols].apply(lambda x: x.str.rstrip())
    data["product_name"] = data["product_name"].str.replace("&", "&", regex=False)

    data[string_cols] = data[string_cols].apply(
        lambda x: x.str.replace(r"&Quot;O&Quot;|\+|\;|\#|Amp|\'039'", "", regex=True)
    )
    data[string_cols] = data[string_cols].apply(
        lambda x: x.str.replace("&039S", "'s", regex=False)
    )
    data[string_cols] = data[string_cols].apply(
        lambda x: x.str.replace("&039", "'", regex=False)
    )
    data[string_cols] = data[string_cols].apply(
        lambda x: x.str.replace("&#039;", "'", regex=False)
    )

    data["product_category"] = data["product_category"].apply(
        lambda x: x[:-3] if isinstance(x, str) and x.endswith(" And") else x
    )
    data.loc[data["product_category"].str.contains("Drug"), "product_category"] = "Drug"
    data.loc[data["product_category"].str.contains("Food"), "product_category"] = "Food"

    data.replace(to_replace={"<NA>": np.nan}, inplace=True)

    return data


def human_format(num):
    """Better formatting of large numbers"""
    num = float(f"{num:.3g}")
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    num = f"{num:f}".rstrip("0").rstrip(".")
    return f"{num}{['', 'K', 'M', 'B', 'T'][magnitude]}"
