# -*- coding: utf-8 -*-
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection


class Database():
    def __init__(self, host, port, collection):
        connections.connect(alias=str(id(self)), host=host, port=port)
        schema = CollectionSchema([
    		FieldSchema("_id", DataType.INT64, is_primary=True),
    		FieldSchema("_data", dtype=DataType.FLOAT_VECTOR, dim=768)
		])
        self.collection = Collection(collection, schema, using=str(id(self)))
        self.createIndex()
    def createIndex(self):
        default_index = {"index_type": "HNSW", "params": {"M": 48, "efConstruction": 50}, "metric_type": "L2"}
        self.collection.create_index(field_name="_data", index_params=default_index)
        self.collection.load()
    def insert(self, did, vector):
        self.collection.insert([
            [did],
            [vector]
        ])
    def query(self, vector, k):
        search_params = {"metric_type": "L2", "params": {"nprobe": 10}}
        res = self.collection.search([vector], "_data", search_params, k)
        return tuple(res[0])
    def get(self, did):
        res = self.collection.query("_id == %d"%did, ["_data"])
        if len(res) < 1:
            return ()
        return tuple(res[0]["_data"])
    def delete(self, did):
        self.collection.delete("_id == %d"%did)