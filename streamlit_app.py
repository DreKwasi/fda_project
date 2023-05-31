import streamlit as st
from st_pages import Page, show_pages
from helper_func import data_parser, styles, aiohttp_func, forms, utils
from streamlit_lottie import st_lottie_spinner


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

styles.local_css("styles/main.css")

show_pages(
    [
        Page("streamlit_app.py", "Product Search", "🕵️"),
        Page("st_pages/analyze.py", "Analytics", "🧮"),
        Page("st_pages/contact.py", "Give Feedback", "✍️"),
        Page("st_pages/newsletter.py", "Join the Newsletter", "✉"),
    ]
)

with st.spinner("Extracting Data from FDA Database ..."):
    with st_lottie_spinner(
        utils.load_lottiefile("assets/animations/wireless_data.json"),
        height=500,
    ):
        aiohttp_func.connect_to_fda()
        # st.sidebar.success("Registered Products Data Uploaded to Database")

data = data_parser.read_data("registered_products.parquet")

if st.experimental_user.email in ["test@localhost.com", "andrewsboateng137@gmail.com"]:
    if st.sidebar.button("Update Data from FDA", type="primary"):
        st.cache_data.clear()
        with st.spinner("Extracting Data from FDA Database ..."):
            with st_lottie_spinner(
                utils.load_lottiefile("assets/animations/wireless_data.json"),
                height=500,
            ):
                aiohttp_func.connect_to_fda()


query_params = st.experimental_get_query_params()

product_index = "all_products"
if query_params:
    try:
        product_index = query_params["product_index"][0]
    except ValueError:
        pass


def product_list_view(data):
    st.sidebar.write("[Click Here to Visit the FDA Registered Products Database](http://196.61.32.245:98/publicsearch)")
    st.sidebar.header("Filter")

    st.sidebar.write("**Select Number of Entries**")
    num = st.sidebar.slider(
        "number_of_entries",
        min_value=5,
        max_value=100,
        value=10,
        label_visibility="collapsed",
        step=10,
    )

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

    st.sidebar.write("**Country Origin**")
    country_origin_list = st.sidebar.multiselect(
        "country_origin",
        options=data["country_origin"].unique(),
        label_visibility="collapsed",
    )
    if country_origin_list:
        data = data[data["country_origin"].isin(country_origin_list)]

    st.header("Welcome To Health Watch 👋")
    st.subheader("Product Search 🔍")
    st.write(
        "This is a Product Indexing/Analytics tool. Search through over 40,000 registered products in Ghana. "
    )
    with st.expander("**DISCLAIMER**"):
        st.write(
            """
The data provided by this tool for fetching registered products from the FDA website is intended for general informational purposes only. While efforts are made to ensure the accuracy and reliability of the information, it is important to note that the data is subject to change and may not always reflect the most current updates.

The Tool updates its database regularly, typically on an hourly basis. However, due to the dynamic nature of the information and potential delays in data synchronization, there may be instances where the data retrieved by this tool is not up-to-date or may not include the latest changes.

It is crucial to understand that this tool does not guarantee the accuracy, completeness, or timeliness of the information provided. Users should exercise their own judgment and verify any information obtained from this tool by cross-referencing it with official sources or contacting the FDA directly.

Furthermore, this tool is not intended to substitute professional advice or guidance from qualified healthcare professionals or regulatory authorities. It is always advisable to consult appropriate sources and experts before making any decisions or taking actions based on the data obtained from this tool.

By using this tool, you acknowledge and accept that the information provided is not exhaustive or definitive. The developers and providers of this tool disclaim any liability for any inaccuracies, errors, omissions, or damages arising from the use or reliance on the information provided by this tool.

Please be aware that the FDA's official website should be considered the primary source of information for the most accurate and up-to-date data regarding registered products.

By proceeding to use this tool, you agree to these terms and conditions and understand the limitations of the data provided."""
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
