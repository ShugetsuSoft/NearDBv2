import grpc
import neardbv2
from concurrent import futures
class NearDBServer():
    def __init__(self, uri, dbhost, dbport, collection, kvdbpath):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
        self.service = neardbv2.service.NearDBService(self.server, dbhost, dbport, collection, kvdbpath)
        self.server.add_insecure_port(uri)
    def run(self):
        self.server.start()
        self.server.wait_for_termination()
        