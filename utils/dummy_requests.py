import requests
import json

# Insert embeddings
url = "http://localhost:5000/api/v1/insert"

payload = json.dumps({
  "celeb_id": 3,
  "img_path": "./data/img_align_celeba/024291.jpg",
  "embedding": [
    -137.12767626,
    83.62350658
  ]
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)


# Search for similar embeddings
url = "http://localhost:5000/api/v1/search"

payload = json.dumps({
  "embedding": [
    -182.55377947,
    56.77146782
  ],
  "max_results": 1
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
