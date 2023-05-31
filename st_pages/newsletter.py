import streamlit as st
from helper_func import utils
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Product Registry",
    page_icon="🛍️",
    initial_sidebar_state="expanded",
    layout="centered",
)



with st.form("signup_form", clear_on_submit=True):
    st.subheader("Receive Data on Registered Products In Your Inbox 😃")
    
    col1, col2 = st.columns([2,1])
    
    with col2:
        lottie_comment = utils.load_lottiefile("assets/animations/coffee.json")

        st_lottie(
            lottie_comment,
            speed=1,
            reverse=False,
            loop=True,
            quality="high",  # medium ; high
            height=100,
            width=None,
            key=None,
        )
    col1.write(
        "**ProductBuddy** sends you weekly updates of Registered Products in your inbox."
    )
    col1.write("**Sign Up to Join the Waitlist** 👇")

    st.write("**Name**")
    name = st.text_input("name", label_visibility="collapsed")

    st.write("**Email**")
    email = st.text_input("email", label_visibility="collapsed")

    submit = st.form_submit_button("Sign Up", type="primary")


if submit:
    pass
