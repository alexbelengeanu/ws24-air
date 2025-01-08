import numpy as np
from tqdm import tqdm

from src.storage.client import DatabaseManager
from src.storage.collection import ImageCollection
from src.storage.dataset import Dataset
from src.embeddings.pretrained import FaceEmbeddings

np.random.seed(7)

# Initialize the database manager object and create the client
db_manager = DatabaseManager()
db_manager.create_client(remove_if_exists=True)

# Initialize the face embeddings object
em = FaceEmbeddings()

# Set up embedding dimension and similarity metric to use
img_dim = 512
img_similarity_metric = "COSINE"
img_collection = ImageCollection(db_manager.get_client(), dimension=img_dim, metric_type=img_similarity_metric)

# Create the dataset object and specify the image folder path and identity map path
dataset = Dataset(
    img_folder_path="./data/img_align_celeba",
    img_identity_map_path="./data/identity_CelebA.txt"
)

img_identity_collection = dataset.images_by_identity()
print('..Started populating vector database...')

# Iterate the identity collection for each celebrity ID
for celebrity_id in tqdm(list(img_identity_collection.keys())):
    celebrity_data = []

    # Iterate the image paths for each celebrity ID
    for img_path in img_identity_collection[celebrity_id]:
       embedding = em.get_embedding(img_path)

       # If the embedding is a numpy array, append the data to the celebrity data list
       if isinstance(embedding, np.ndarray):
           celebrity_data.append({
               'celeb_id': celebrity_id,
               'img_path': img_path,
               'vector': embedding
           })

    query_result = img_collection.insert(celebrity_data)

print('..Finished populating vector database...')
