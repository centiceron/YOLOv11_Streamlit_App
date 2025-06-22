#Importing libs
import streamlit as st
from streamlit_option_menu import option_menu
import main, signup, account, home

#page layout
st.set_page_config(
    page_title="Welcome to my first Streamlit app",
    page_icon=':home:'
)

with st.sidebar:
    st.sidebar.subheader("Welcome back, user!!")
    app = option_menu(
        menu_title="Menu",
        options=['Home','Account','App','Sign up'],
        icons=['house-fill','person-circle','app','info'],
        default_index=1
    )

#Login dialog
@st.dialog("Login to your account")
def signin():
    with st.form('login', border=True, width="stretch", height="content"):
        email = st.text_input('Email address')
        password = st.text_input('Password')
        st.form_submit_button('Sign In')

if app == 'Home':
    st.subheader("This is the home page of my app, you may head over to the App page to access the YOLOv11 model for object detection and various other model configurations")
if app == 'App':
        main.app()
if app == 'Sign up':
        signin()
if app == 'Account':
        account.app()




