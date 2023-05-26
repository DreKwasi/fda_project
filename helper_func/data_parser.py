import pandas as pd
import numpy as np
import streamlit as st
from .firestore_func import download_blob
import time


# @st.cache_data(show_spinner="Parsing Data ... ")
def read_data(filename):
    # start = time.perf_counter()
    df = download_blob(f"data/{filename}", f"assets/{filename}")
    # end = time.perf_counter()
    # print(f"Download Time: {end - start}")

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
    data[string_cols] = data[string_cols].apply(lambda x: x.str.strip())
    data["product_name"] = (
        data["product_name"].str.replace(r"&Quot;O&Quot;|\+", '', regex=True)
    )

    data["product_category"] = data["product_category"].apply(
        lambda x: x[:-3] if isinstance(x, str) and x.endswith(" And") else x
    )

    # data.fillna("Not Specified", inplace=True)
    # 2023-04-11T14:51:18.000000Z
    data["created_at"] = pd.to_datetime(data["created_at"], format="ISO8601")
    data["updated_at"] = pd.to_datetime(data["updated_at"], format="ISO8601")

    data = data.assign(registration_date=data["registration_date"].astype(str)[:10])
    data = data.assign(expiry_date=data["expiry_date"].astype(str)[:10])

    data.replace(to_replace={"<NA>": np.nan}, inplace=True)

    data["registration_date"] = pd.to_datetime(
        data["registration_date"], yearfirst=True, format="mixed"
    )
    data["expiry_date"] = pd.to_datetime(
        data["expiry_date"], yearfirst=True, format="%Y-%m-%d"
    )

    return data
