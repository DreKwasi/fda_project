import streamlit as st


def filter_widgets(df):
    date_cols = ["registration_date", "expiry_date", "created_at", "updated_at"]

    st.sidebar.write("**Filter Date By:**")
    date_col = st.sidebar.selectbox(
        "date_col", key="date_col", options=date_cols, label_visibility="collapsed"
    )
    df = df[~(df[date_col].isna())]
    min_date, max_date = df[date_col].dt.date.min(), df[date_col].dt.date.max()

    start_col, end_col = st.sidebar.columns(2)
    with start_col:
        st.write("**Start Date**")
        start_date = st.date_input(
            "start_date",
            value=min_date,
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
        )
    with end_col:
        st.write("**End Date**")
        end_date = st.date_input(
            "end_date",
            value=max_date,
            min_value=min_date,
            max_value=max_date,
            label_visibility="collapsed",
        )

    if start_date > end_date:
        st.error("Start Date Can Not be Greater than End Date")
        st.stop()

    product_status = df["status"].unique()
    st.sidebar.write("**Product Status**")
    sel_order_status = st.sidebar.multiselect(
        "status",
        key="status",
        options=product_status,
        label_visibility="collapsed",
    )

    prod_category = df["product_category"].unique()
    st.sidebar.write("**Product Categories**")
    sel_prod_category = st.sidebar.multiselect(
        label="prod_category",
        key="prod_category",
        options=prod_category,
        label_visibility="collapsed",
    )

    applicants = df["applicant"].unique()
    st.sidebar.write("**Applicant**")
    sel_applicant = st.sidebar.multiselect(
        "filter_applicant",
        key="filter_applicant",
        options=applicants,
        label_visibility="collapsed",
    )

    manufacturers = df["manufacturer"].unique()
    st.sidebar.write("**Manufacturer**")
    sel_manufacturer = st.sidebar.multiselect(
        "manufacturer",
        key="manufacturer",
        options=manufacturers,
        label_visibility="collapsed",
    )
    country = df["country_origin"].unique()
    st.sidebar.write("**Country Origin**")
    sel_country = st.sidebar.multiselect(
        "country_origin",
        key="country_origin",
        options=country,
        label_visibility="collapsed",
    )

    filters = [
        date_col,
        start_date,
        end_date,
        sel_order_status,
        sel_prod_category,
        sel_applicant,
        sel_manufacturer,
        sel_country,
    ]

    return filters


@st.cache_data(show_spinner=False)
def filter_data(
    df,
    date_col,
    start_date,
    end_date,
    sel_order_status,
    sel_prod_category,
    sel_applicant,
    sel_manufacturer,
    sel_country,
):
    date_filter = (df[date_col].dt.date >= start_date) & (
        df[date_col].dt.date <= end_date
    )
    df = df[date_filter]

    if len(sel_order_status) > 0:
        df = df[df["status"].isin(sel_order_status)]

    if len(sel_prod_category) > 0:
        df = df[df["product_category_name"].isin(sel_prod_category)]

    if len(sel_applicant) > 0:
        df = df[df["applicant"].isin(sel_applicant)]

    if len(sel_manufacturer) > 0:
        df = df[df["manufacturer"].isin(sel_manufacturer)]

    if len(sel_country) > 0:
        df = df[df["country_origin"].isin(sel_country)]

    return df
