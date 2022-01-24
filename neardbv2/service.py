# -*- coding: utf-8 -*-
from neardbv2 import pb
from neardbv2 import database
import numpy
from neardbv2 import transform

class NearDBService(pb.pb_pb2_grpc.NearDBService):
    def __init__(self, server, milvus_host, milvus_port, collection, bert_service_host):
        self.database = database.Database(milvus_host, milvus_port, collection)
        self.transform = transform.Transform(bert_service_host)
        pb.pb_pb2_grpc.add_NearDBServiceServicer_to_server(self, server)
    def Add(self, request, context):
        feature = self.transform.getTagsFeature(list(request.taglist))
        self.database.insert(request.id, feature)
        return pb.pb_pb2.NoneResponse()
    def Query(self, request, context):
        feature = self.transform.getTagsFeature(list(request.taglist))
        if request.drift != 0:
            feature += numpy.random.normal(0,request.drift,768)
        results = self.database.query(feature, request.k)
        return pb.pb_pb2.QueryResponse(items=[pb.pb_pb2.Item(id=result.id, distance=result.distance) for result in results])
    def Remove(self, request, context):
        self.database.delete(request.id)