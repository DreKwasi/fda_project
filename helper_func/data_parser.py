import pandas as pd
import numpy as np
import streamlit as st
from .firestore_func import download_blob


# @st.cache_data(show_spinner="Parsing Data ... ")
def read_data(filename):
    data = download_blob(f"data/{filename}", f"assets/{filename}")
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
