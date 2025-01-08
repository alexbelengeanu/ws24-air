import streamlit as st
from src.frontend.utils import insert_celebrity_picture
from src.frontend.utils import search_similar_celebrity

option = st.sidebar.selectbox("Choose Action", ["Insert Celebrity", "Search Celebrity"])

# Insert Celebrity
if option == "Insert Celebrity":
    st.header("Insert Celebrity")
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    if st.button("Insert"):
        try:
            response = insert_celebrity_picture(img_path)
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")

# Search for similar celebrity
if option == "Search Celebrity":
    st.header("Search Celebrity")
    max_results = st.number_input("Max Results", min_value=1, step=1, value=1)
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    
    if st.button("Search"):
        try:
            response = search_similar_celebrity(img_path, max_results)
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")
