from pymilvus import MilvusClient

from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from src.api import DatabaseManager, get_manager
from ..lifetime import ImageCollection, get_collection
from ..settings import app_settings

import numpy as np
np.random.seed(7)

router = APIRouter(tags=["Query"])


@router.post(
    "/insert/dummy",
    status_code=status.HTTP_200_OK,
    description="This endpoint should be used for testing or debugging purposes only. It inserts dummy data into the"
                " vector database.",
)
async def insert_dummy_embedding(
        img_collection: ImageCollection = Depends(get_collection)
) -> JSONResponse:
    """
    The endpoint responsible for inserting new incoming dummy images in the Vector database.

    :param img_collection: ImageCollection
    """
    from src.storage.dataset import Dataset
    dataset = Dataset(
        img_folder_path=app_settings.celeb_img_folder_path,
        img_identity_map_path=app_settings.celeb_identity_map_path
    )

    img_identity_collection = dataset.images_by_identity()
    keys_list = list(img_identity_collection.keys())
    for key in keys_list[:2]:  # Using slicing to get the first five keys
        print(f'{key}: {img_identity_collection[key]}\n')

    id1_images = img_identity_collection[keys_list[0]]
    id2_images = img_identity_collection[keys_list[1]]

    dummy_data = []
    dummy_data.extend(
        [
            {
                'celeb_id': keys_list[0],
                'img_path': img_path,
                'vector': embedding_celebrity_id1(img_path, dim=app_settings.embedding_dim)
            }
            for img_path in id1_images[:3]
        ]
    )
    dummy_data.extend(
        [
            {
                'celeb_id': keys_list[1],
                'img_path': img_path,
                'vector': embedding_celebrity_id2(img_path, dim=app_settings.embedding_dim)
            }
            for img_path in id2_images[:3]
        ]
    )

    img_collection.insert(dummy_data)


    return JSONResponse(
        content={
            'status': 'Successfully inserted dummy data.'
        },
    )



@router.post(
    "/search/dummy",
    status_code=status.HTTP_200_OK,
    description="This endpoint should be used for testing or debugging purposes only. It searches for the closest "
                "embedding that matches the dummy uploaded embeddings.",
)
async def search_dummy_embedding(
        img_collection: ImageCollection = Depends(get_collection)
) -> StreamingResponse:
    """
    The endpoint responsible for searching for the closest dummy images in the Vector database.

    :param img_collection: ImageCollection
    """

    query_vector = embedding_celebrity_id1("uploaded_image.jpg", dim=app_settings.embedding_dim)
    hits = img_collection.search(query_vectors=[query_vector], limit=app_settings.max_results)

    # Dictionary to store the results
    result_dict = {}

    # Iterate through the list with an index
    for index, item in enumerate(hits, start=1):
        key = f'hit_{index}'
        result_dict[key] = item

    return JSONResponse(
        content=result_dict,
    )


@router.post(
    "/insert",
    status_code=status.HTTP_200_OK,
    description="Use this endpoint if you want to push real new incoming images into the Vector database.",
)
async def insert_embedding(
        request: Request,
        img_collection: ImageCollection = Depends(get_collection)
) -> JSONResponse:
    """
    The endpoint responsible for inserting new incoming images in the Vector database.

    :param request: Request
    :param img_collection: ImageCollection
    """

    # Get the image embedding from the request
    data = await request.json()
    input_data = {
            'celeb_id': int(data['celeb_id']),
            'img_path': data['img_path'],
            'vector': np.array(data['embedding'])
        }

    img_collection.insert([input_data])

    return JSONResponse(
        content={
            'status': f'Successfully inserted data for celebrity id {data["celeb_id"]} with image '
                      f'located at {data["img_path"]}.'
        },
    )


@router.post(
    "/search",
    status_code=status.HTTP_200_OK,
    description="Use this endpoint if you want to search for the closest embedding that matches the uploaded embeddings.",
)
async def search_embedding(
        request: Request,
        img_collection: ImageCollection = Depends(get_collection)
) -> StreamingResponse:
    """
    The endpoint responsible for searching for the closest images in the Vector database.

    :param request: Request
    :param img_collection: ImageCollection
    """
    data = await request.json()

    hits = img_collection.search(query_vectors=[np.array(data['embedding'])], limit=int(data['max_results']))

    # Dictionary to store the results
    result_dict = {}

    # Iterate through the list with an index
    for index, item in enumerate(hits, start=1):
        key = f'hit_{index}'
        result_dict[key] = item

    return JSONResponse(
        content=result_dict,
    )


def embedding_celebrity_id1(img_path: str, dim: int):
    vector = np.random.normal(size=dim, loc=[100, 100], scale=10)
    return vector

def embedding_celebrity_id2(img_path: str, dim: int):
    vector = np.random.normal(size=dim, loc=[-100, 30], scale=50)
    return vector