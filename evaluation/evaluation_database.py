import numpy as np
from tqdm import tqdm

from src.storage.client import DatabaseManager
from src.storage.collection import ImageCollection
from src.storage.dataset import Dataset
from src.embeddings.pretrained import FaceEmbeddings

def create_evaluation_database(n: int) -> tuple[DatabaseManager, dict]:
    np.random.seed(7)

    db_manager = DatabaseManager(db_name="evaluation.db")
    db_manager.create_client(remove_if_exists=True)
    em = FaceEmbeddings()

    img_dim = 512
    img_similarity_metric = "COSINE"
    img_collection = ImageCollection(db_manager.get_client(), dimension=img_dim, metric_type=img_similarity_metric)

    dataset = Dataset(
        img_folder_path="./data/img_align_celeba",
        img_identity_map_path="./data/identity_CelebA.txt"
    )

    img_identity_collection = dataset.images_by_identity()
    img_identity_collection = {celeb_id: images for celeb_id, images in img_identity_collection.items() if len(images) > 5}
    
    celebrity_ids_shuffled = list(img_identity_collection.keys())
    np.random.shuffle(celebrity_ids_shuffled)

    celebrity_data = []
    test_data = {}

    n_selected = 0
    faulty_ids = []
    with tqdm(total=n) as pbar:
        for celebrity_id in celebrity_ids_shuffled:
            img_paths = img_identity_collection[celebrity_id]
            temp_celebrity_data = []
            temp_test_data = []

            faulty = False
            test_paths = np.random.choice(img_paths, 1, replace=False)
            train_paths = list(set(img_paths) - set(test_paths))

            for img_path in train_paths:
                embedding = em.get_embedding(img_path)
                if isinstance(embedding, np.ndarray):
                    temp_celebrity_data.append({
                        'celeb_id': celebrity_id,
                        'img_path': img_path,
                        'vector': embedding
                    })
                else:
                    faulty = True
                    break

            for img_path in test_paths:
                embedding = em.get_embedding(img_path)
                if isinstance(embedding, np.ndarray):
                    temp_test_data.append({
                        'celeb_id': celebrity_id,
                        'img_path': img_path,
                        'vector': embedding
                    })
                else:
                    faulty = True
                    break

            if faulty == True:
                faulty_ids.append(celebrity_id)
                continue

            n_selected += 1
            celebrity_data.extend(temp_celebrity_data)
            test_data[celebrity_id] = temp_test_data
            pbar.update(1)

            if n_selected == n:
                break
        
    img_collection.insert(celebrity_data)

    return db_manager, test_data