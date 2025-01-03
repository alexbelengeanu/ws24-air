from pymilvus import MilvusClient, DataType
from typing import Union, List


class ImageCollection():
    client: MilvusClient
    collection_name: str = "images"
    dimension: int

    def __init__(self, client: MilvusClient, dimension: int, metric_type: str):
        self.client = client
        self.dimension = dimension

        schema, index_params = self.schema(vector_dim=dimension, metric_type=metric_type)

        client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=index_params
        )
        
    def schema(self, vector_dim: int, metric_type: str):
        schema = self.client.create_schema(
                auto_id=True,
                enable_dynamic_field=True,
            )

        schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
        schema.add_field(field_name="celeb_id", datatype=DataType.INT64)
        schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=vector_dim)
        schema.add_field(field_name="img_path", datatype=DataType.VARCHAR, max_length=512)

        index_params = self.client.prepare_index_params()

        # index_params.add_index(
        #     field_name="celeb_id",
        #     index_type="AUTOINDEX"
        # )

        index_params.add_index(
            field_name="vector", 
            index_type="AUTOINDEX",
            metric_type=metric_type
        )

        return schema, index_params




    def insert(self, data: list[object]):
        """
        Insert list of objects with schema {'celeb_id': int, 'img_path': string, 'vector': [[embedding_dimension]]}

        Args:
            data (list[list[object]]): A list of data objects to be inserted into the collection.

        Returns:
            None
        """

        for record in data:
            assert "celeb_id" in record
            assert "img_path" in record
            assert "vector" in record
            assert len(record['vector']) == self.dimension

        res = self.client.insert(collection_name=self.collection_name, data=data)

        return res

    def search(self, query_vectors: Union[List[list], list], limit: int = 10):
        res = self.client.search(
            collection_name=self.collection_name,
            anns_field="vector",
            data=query_vectors,
            limit=limit,
            output_fields=["vector", "celeb_id", "img_path"]
        )

        return res
