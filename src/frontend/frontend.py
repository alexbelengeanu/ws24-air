import streamlit as st
import requests
import json
import uuid

# Sidebar for navigation
option = st.sidebar.selectbox("Choose Action", ["Insert Celebrity", "Search Celebrity"])

# Insert Celebrity
if option == "Insert Celebrity":
    st.header("Insert Celebrity")
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    embedding = st.text_area("Embedding (comma-separated)", "-137.12767626, 83.62350658")
    
    if st.button("Insert"):
        try:
            embedding_list = [float(x.strip()) for x in embedding.split(',')]
            # payload = {
            #     "celeb_id": celeb_id,
            #     "img_path": img_path,
            #     "embedding": embedding_list
            # }

            payload = json.dumps({
                     # unique celebrity ID
                      "celeb_id": str(uuid.uuid4()),
                      "img_path": img_path,
                      "embedding": embedding_list
                    })
            headers = {
              'Content-Type': 'application/json'
            }
            response = requests.post("http://localhost:5000/api/v1/insert", headers=headers, data=payload)
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")

# Search for similar celebrity
if option == "Search Celebrity":
    st.header("Search Celebrity")
    embedding = st.text_area("Embedding (comma-separated)", "-182.55377947, 56.77146782")
    max_results = st.number_input("Max Results", min_value=1, step=1, value=1)
    
    if st.button("Search"):
        try:
            embedding_list = [float(x.strip()) for x in embedding.split(',')]
            payload = {
                "embedding": embedding_list,
                "max_results": max_results
            }
            response = requests.post("http://localhost:5000/api/v1/search", json=payload)
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")
