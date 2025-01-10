import streamlit as st
from PIL import Image
from src.frontend.utils import insert_celebrity_picture
from src.frontend.utils import search_similar_celebrity
from src.frontend.utils import image_to_base64
import time

if "is_first_run" not in st.session_state:
    st.session_state.is_first_run = True  # Set to True only the first time

if st.session_state.is_first_run:
    st.markdown("## Welcome to FindMyTwin!")
    st.markdown("Have you ever wondered who your celebrity twin is?")
    st.markdown("Well, you're in luck! Our machine learning model will decide that for you!")
    logo = Image.open("./src/frontend/logo/logo.png")
    img_base64 = image_to_base64(logo)
    st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_base64}' width='500'/></div>", unsafe_allow_html=True)
    st.session_state.is_first_run = False

if 'selected_action' not in st.session_state:
    st.session_state.selected_action = None

st.sidebar.markdown("<h3>Choose Action</h3>", unsafe_allow_html=True)

if st.sidebar.button("Insert Celebrity"):
    st.session_state.selected_action = "Insert Celebrity"
if st.sidebar.button("Find My Twin"):
    st.session_state.selected_action = "Find My Twin"



if st.session_state.selected_action == "Insert Celebrity":
    st.header("Insert Celebrity")
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    
    if st.button("Insert"):
        try:
            response = insert_celebrity_picture(img_path)
            you = Image.open(img_path)
            st.markdown("<h3 style='text-align: center;'>Inserted image:</h3>", unsafe_allow_html=True)
            img_base64 = image_to_base64(you)
            st.markdown(f"<div style='text-align: center;'><img src='data:image/png;base64,{img_base64}' width='300'/></div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Error: {e}")

if st.session_state.selected_action == "Find My Twin":
    st.header("Find My Twin")
    max_results = st.number_input("Max Results", min_value=1, step=1, value=1)
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    
    if st.button("Search"):
        try:
            you = Image.open(img_path)
            st.markdown("<h3 style='text-align: center;'>Searching for your twin... Please wait.</h3>", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.image(you, caption="Uploaded Image", use_container_width=True)

            response = search_similar_celebrity(img_path, max_results)
            time.sleep(3)
            twin = Image.open(response)
            with col2:
                st.image(twin, caption="Your Twin", use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
