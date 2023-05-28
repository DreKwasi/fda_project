import streamlit as st
from helper_func import data_parser, styles, utils
from streamlit_lottie import st_lottie  # pip install streamlit-lottie


st.set_page_config(
    page_title="Product Registry",
    page_icon="🛍️",
    initial_sidebar_state="expanded",
    layout="wide",
)

styles.local_css("styles/main.css")
styles.local_css("styles/contact_form.css")

st.header("📥 Get In Touch With Me !")
col1, col2 = st.columns([2, 1])
contact_form = """
<form action="https://formsubmit.co/f019594dc785ee264df1d144b7593265 " method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here"></textarea>
     <button type="submit">Send</button>
</form>
"""
col1.markdown(contact_form, unsafe_allow_html=True)

lottie_comment = utils.load_lottiefile("assets/animations/email_us.json")

with col2:
    st_lottie(
        lottie_comment,
        speed=1,
        reverse=False,
        loop=True,
        quality="high", # medium ; high
        height=500,
        width=None,
        key=None,
    )