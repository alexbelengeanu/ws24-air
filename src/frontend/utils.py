from src.embeddings.pretrained import FaceEmbeddings
from src.storage.dataset import Dataset
from random import randint
import requests
import json

import base64
import io
from PIL import Image

em = FaceEmbeddings()

dataset = Dataset(
    img_folder_path="./data/img_align_celeba",
    img_identity_map_path="./data/identity_CelebA.txt"
)

img_identity_collection = dataset.images_by_identity()

# url = "http://localhost:5000/api/v1/insert"

def insert_celebrity_picture(img_path):
  # randint(1, 999999)
  payload = json.dumps({
              # unique celebrity ID
              "celeb_id": 12345678,
              "img_path": img_path,
              "embedding": em.get_embedding(path=img_path).tolist()
            })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.request("POST", "http://localhost:5000/api/v1/insert", headers=headers, data=payload)
  return response
# response.json()['status'].split('located at ')[1].strip('.')


# url = "http://localhost:5000/api/v1/search"

def search_similar_celebrity(src_img_path, max_results):
  embedding = em.get_embedding(path=src_img_path)
  # with open("/home/teuo/Documents/uni_files/Wintersemester_TUG/WS2023/AS/algosandgames/out.txt", "w") as file:
  #   file.write(embedding)


  payload = json.dumps({
            "embedding": embedding.tolist(),
            "max_results": max_results
          })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", "http://localhost:5000/api/v1/search", headers=headers, data=payload)
  return response.json()["hit_1"][0]["entity"]["img_path"]


def image_to_base64(img):
    buffered = io.BytesIO() 
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")  # Convert to base64 string
    return img_base64