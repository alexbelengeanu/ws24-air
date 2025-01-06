import numpy as np
from tqdm import tqdm

from src.storage.client import DatabaseManager
from src.storage.collection import ImageCollection
from src.storage.dataset import Dataset

np.random.seed(7)

# Initialize the database manager object and create the client
db_manager = DatabaseManager()
db_manager.create_client(remove_if_exists=True)

# Set up embedding dimension and similarity metric to use
img_dim = 2
img_similarity_metric = "COSINE"
img_collection = ImageCollection(db_manager.get_client(), dimension=img_dim, metric_type=img_similarity_metric)

# Create the dataset object and specify the image folder path and identity map path
dataset = Dataset(
    img_folder_path="./data/img_align_celeba",
    img_identity_map_path="./data/identity_CelebA.txt"
)

dummy_data = []

print('..Started populating vector database...')
img_identity_collection = dataset.images_by_identity()

# Iterate the identity collection for each celebrity ID
for celebrity_id in tqdm(list(img_identity_collection.keys())):

    # Extend the data list with the celebrity ID, image path and a random vector (for now)
    dummy_data.extend(
        [
            {
                'celeb_id': celebrity_id,
                'img_path': img_path,
                'vector': np.random.normal(size=2, loc=[100, 100], scale=10) #TODO: replace with actual vector embedding
             }
            for img_path in img_identity_collection[celebrity_id]
        ]
    )

    # Break after the first celebrity ID just to make sure it works as expected
    break

# Insert the dummy data into the vector database
query_result = img_collection.insert(dummy_data)

print(f'..Successfully inserted {query_result["insert_count"]} records into the vector database...')
