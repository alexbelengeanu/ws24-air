from src.embeddings.pretrained import FaceEmbeddings
from src.storage.dataset import Dataset
import uuid
import requests
import json

em = FaceEmbeddings()

dataset = Dataset(
    img_folder_path="./data/img_align_celeba",
    img_identity_map_path="./data/identity_CelebA.txt"
)

img_identity_collection = dataset.images_by_identity()

url = "http://localhost:5000/api/v1/insert"

def insert_celebrity_picture(img_path):
  payload = json.dumps({
              # unique celebrity ID
              "celeb_id": str(uuid.uuid4()),
              "img_path": img_path,
              "embedding": em.get_embedding(path=img_path)
            })
  headers = {
    'Content-Type': 'application/json'
  }
  response = requests.post(url, headers=headers, data=payload)
  return response


url = "http://localhost:5000/api/v1/search"

def search_similar_celebrity(src_img_path, max_results):
  payload = json.dumps({
            "embedding": em.get_embedding(path=src_img_path),
            "max_results": max_results
          })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.post(url, headers=headers, data=payload)
  return response