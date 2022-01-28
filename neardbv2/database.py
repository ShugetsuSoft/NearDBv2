# -*- coding: utf-8 -*-
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import plyvel
import msgpack
import msgpack_numpy as m
m.patch()

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
    
def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

class Database():
    def __init__(self, host, port, collection, kvdbpath):
        connections.connect(alias=str(id(self)), host=host, port=port)
        schema = CollectionSchema([
    		FieldSchema("_id", DataType.INT64, is_primary=True),
    		FieldSchema("_data", dtype=DataType.FLOAT_VECTOR, dim=768)
		])
        self.kvdb = plyvel.DB(kvdbpath, create_if_missing=True)
        self.collection = Collection(collection, schema, using=str(id(self)))
        self.collection.load()
    def createIndex(self):
        default_index = {"index_type": "HNSW", "params": {"M": 48, "efConstruction": 50}, "metric_type": "L2", "nlist": 4096}
        self.collection.create_index(field_name="_data", index_params=default_index)
        self.collection.load()
    def insert(self, did, vector):
        self.kvdb.put(int_to_bytes(did), msgpack.packb(vector))
        self.collection.insert([
            [did],
            [vector]
        ])
    def query(self, vector, k):
        search_params = {"metric_type": "L2", "params": {"nprobe": 128}}
        res = self.collection.search([vector], "_data", search_params, k)
        return tuple(res[0])
    def get(self, did):
        res = self.kvdb.get(int_to_bytes(did))
        if res:
            res = msgpack.unpackb(res)
            return tuple(res)
        return ()
    def delete(self, did):
        self.kvdb.delete(int_to_bytes(did))
        self.collection.delete("_id == %d"%did)