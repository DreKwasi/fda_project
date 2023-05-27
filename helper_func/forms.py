import streamlit as st


def detailed_view(data, product_index):
    if st.button("Go Back"):
        st.experimental_set_query_params(product_index="all_products")
        st.experimental_rerun()
    data = data.iloc[int(product_index), :].values.tolist()
    st.subheader("Product Details")
    st.write(data)
