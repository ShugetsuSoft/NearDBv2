# -*- coding: utf-8 -*-
from neardbv2 import pb
from neardbv2 import database
from neardbv2 import transform
from lru import LRU

class NearDBService(pb.pb_pb2_grpc.NearDBService):
    def __init__(self, server, milvus_host, milvus_port, bert_service_host):
        self.database = database.Database(milvus_host, milvus_port)
        self.transform = transform.Transform(bert_service_host)
        self.cache = LRU(200)
        pb.pb_pb2_grpc.add_NearDBServiceServicer_to_server(self, server)
    def Add(self, request, context):
        print(request.id)
        print(request.taglist)
        feature = self.transform.getTagsFeature(request.taglist)
        self.database.insert(request.id, feature)
        return pb.pb_pb2.NoneResponse()
    def Query(self, request, context):
        if tuple(request.taglist) + (request.k,) in self.cache:
            results = self.cache[tuple(request.taglist) + (request.k,)]
        else:
            feature = self.transform.getTagsFeature(request.taglist)
            results = self.database.query(feature, request.k)
            self.cache[tuple(request.taglist) + (request.k,)] = results
        return pb.pb_pb2.QueryResponse(items=[pb.pb_pb2.Item(id=result.id, distance=result.distance) for result in results])
    def QueryPage(self, request, context):
        if tuple(request.taglist) + (request.all,) in self.cache:
            results = self.cache[tuple(request.taglist) + (request.all,)]
            print("Query", request.taglist, "range from", request.offset, "to", request.offset + request.k)
            if request.offset + request.k < len(results):
                return pb.pb_pb2.QueryResponse(items=[pb.pb_pb2.Item(id=result.id, distance=result.distance) for result in results[request.offset : request.offset + request.k]])
            raise Exception("Offset Exceed All")
        feature = self.transform.getTagsFeature(tuple(request.taglist))
        results = self.database.query(feature, request.all)
        self.cache[tuple(request.taglist) + (request.all,)] = results
        return pb.pb_pb2.QueryResponse(items=[pb.pb_pb2.Item(id=result.id, distance=result.distance) for result in results[request.offset : request.offset + request.k]])
    def Remove(self, request, context):
        self.database.delete(request.id)