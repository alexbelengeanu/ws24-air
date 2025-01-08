import streamlit as st
import requests
import json
import uuid
import os
import sys
from src.embeddings.pretrained import FaceEmbeddings
from src.storage.dataset import Dataset

# print("Current Working Directory:", os.getcwd())

# # Print Python path
# print("Python Path:", sys.path)

# Sidebar for navigation
option = st.sidebar.selectbox("Choose Action", ["Insert Celebrity", "Search Celebrity"])

em = FaceEmbeddings()

dataset = Dataset(
    img_folder_path="./data/img_align_celeba",
    img_identity_map_path="./data/identity_CelebA.txt"
)

img_identity_collection = dataset.images_by_identity()

# Insert Celebrity
if option == "Insert Celebrity":
    st.header("Insert Celebrity")
    img_path = st.text_input("Image Path", value="./data/img_align_celeba/024291.jpg")
    if st.button("Insert"):
        try:
            payload = json.dumps({
                     # unique celebrity ID
                      "celeb_id": str(uuid.uuid4()),
                      "img_path": img_path,
                      "embedding": em.get_embedding(path=img_path)
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
    max_results = st.number_input("Max Results", min_value=1, step=1, value=1)
    
    if st.button("Search"):
        try:
            payload = json.dumps({
                      "embedding": em.get_embedding(path=img_path),
                      "max_results": max_results
                    })
            headers = {
              'Content-Type': 'application/json'
            }

            response = requests.post("http://localhost:5000/api/v1/search", headers=headers, data=payload)
            st.json(response.json())
        except Exception as e:
            st.error(f"Error: {e}")
