import streamlit as st
import json


# GitHub: https://github.com/andfanilo/streamlit-lottie
# Lottie Files: https://lottiefiles.com/


@st.cache_data(show_spinner=False)
def convert_df(df):
    return df.to_csv(index=False).encode("utf-8")


def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

def pagination(data, num):
    st.session_state.page_number_one = (
        0
        if "page_number_one" not in st.session_state
        else st.session_state.page_number_one
    )
    if num <= data.shape[0]:
        if data.shape[0] % num == 0:
            last_page = data.shape[0] // num
        else:
            last_page = (data.shape[0] // num) + 1
    else:
        num = data.shape[0]
        last_page = 1

    st.session_state.page_number_one = (
        last_page
        if st.session_state.page_number_one > last_page
        else st.session_state.page_number_one
    )

    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    if col1.button("Previous Page ⬅️"):
        if st.session_state.page_number_one - 1 < 0:
            st.session_state.page_number_one = last_page
        else:
            st.session_state.page_number_one -= 1
    if col2.button("Next Page ➡️"):
        if st.session_state.page_number_one + 1 > last_page:
            st.session_state.page_number_one = 0
        else:
            st.session_state.page_number_one += 1

    if col3.button("First Page 🔝"):
        st.session_state.page_number_one = 0

    if col4.button("Last Page 🔙"):
        st.session_state.page_number_one = last_page

    st.caption(f"Page {st.session_state.page_number_one + 1} Out of {last_page}")

    start_index = st.session_state.page_number_one * num
    end_index = (
        (1 + st.session_state.page_number_one) * num
        if st.session_state.page_number_one != 0
        else num
    )

    return start_index, end_index
