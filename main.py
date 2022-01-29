import server
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')
if "server" in config:
    seraddr = config["server"]["listen"]
else:
    seraddr = "0.0.0.0:9888"

if "milvus" in config:
    milvusHost = config["milvus"]["host"]
    milvusPort = config["milvus"]["port"]
    collection = config["milvus"]["collection"]
else:
    milvusHost = "127.0.0.1"
    milvusPort = "19530"
    collection = "neardb_vec"

if "database" in config:
    etcdhost = config["database"]["etcdhost"]
    etcdport = config["database"]["etcdport"]
else:
    etcdhost = "localhost"
    etcdport = 2379

if "bert" in config:
    berthost = config["bert"]["host"]
else:
    berthost = "localhost"

ser = server.NearDBServer(seraddr, milvusHost, milvusPort, collection, etcdhost, etcdport, berthost)
ser.run()
