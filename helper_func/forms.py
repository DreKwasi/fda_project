import streamlit as st
import datetime as dt
import pandas as pd


def detailed_view(data, product_index):
    if st.button("View All Products", type="primary"):
        st.experimental_set_query_params(product_index="all_products")
        st.experimental_rerun()
    data = data.iloc[int(product_index), :]

    st.header(f"{data['product_name']}", anchor=False)

    days_to_expiry = (data["expiry_date"] - dt.datetime.now()).days
    col1, col2, col3 = st.columns(3)

    # Display "Days To Expiry" with the number of days or "Not Specified" if the expiry date is missing
    if pd.isnull(data["expiry_date"]):
        col1.write("Days To Expiry: Not Specified")
    else:
        col1.write(f"Days To Expiry: {days_to_expiry}")

    # Display "Registration Date" or "Not Specified" if the registration date is missing
    if pd.isnull(data["registration_date"]):
        col2.write("Registration Date: Not Specified")
    else:
        col2.write(
            f"Registration Date: {data['registration_date'].strftime('%d %b, %Y')}"
        )

    # Display "Expiry Date" or "Not Specified" if the expiry date is missing
    if pd.isnull(data["expiry_date"]):
        col3.write("Expiry Date: Not Specified")
    else:
        col3.write(f"Expiry Date: {data['expiry_date'].strftime('%d %b, %Y')}")

    st.subheader("Product Information", anchor=False)
    col1, col2, col3, col4 = st.columns(4)
    col1.write("<h5> <u> Product ID </u> </h5>", unsafe_allow_html=True)
    col1.write(f"***{data['product_id']}***")

    col2.write("<h5> <u> Registration Number </u> </h5>", unsafe_allow_html=True)
    col2.write(f"***{data['registration_number']}***")

    col3.write("<h5> <u> Product Category </u> </h5>", unsafe_allow_html=True)
    col3.write(f"***{data['product_category']}***")

    col4.write("<h5> <u> Product Sub Category </u> </h5>", unsafe_allow_html=True)
    col4.write(f"***{data['product_sub_category']}***")

    col1, col2, col3, col4 = st.columns(4)

    col1.write("<h5> <u> Generic Name </u> </h5>", unsafe_allow_html=True)
    col1.write(f"***{data['generic_name']}***")

    col2.write("<h5> <u> Active Ingredient </u> </h5>", unsafe_allow_html=True)
    col2.write(f"***{data['active_ingredient']}***")

    col3.write("<h5> <u> Strength </u> </h5>", unsafe_allow_html=True)
    col3.write(f"***{data['strength']}***")

    col4.write("<h5> <u> Dosage Form Indication </u> </h5>", unsafe_allow_html=True)
    col4.write(f"***{data['dosage_form_indication']}***")

    st.divider()

    st.write("#### Applicant/Client Information")
    col1, col2, col3 = st.columns(3)

    col1.write("<h5> <u> Client Name </u> </h5>", unsafe_allow_html=True)
    col1.write(f"***{data['client_name']}***")

    col2.write("<h5> <u> Email </u> </h5>", unsafe_allow_html=True)
    col2.write(f"***{data['email']}***")

    col3.write("<h5> <u> Postal Address </u> </h5>", unsafe_allow_html=True)
    col3.write(f"***{data['postal_address']}***")

    col1, col2, col3 = st.columns(3)

    col1.write("<h5> <u> Registered Importers </u> </h5>", unsafe_allow_html=True)
    col1.write(f"***{data['registerd_importers']}***")

    col2.write("<h5> <u> Manufacturer </u> </h5>", unsafe_allow_html=True)
    col2.write(f"***{data['manufacturer']}***")

    col3.write("<h5> <u> Country of Origin (Region) </u> </h5>", unsafe_allow_html=True)
    col3.write(f"***{data['country_origin'], (data['region'])}***")
