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
    kvdbpath = config["database"]["kvpath"]
else:
    kvdbpath = "vectors.db"

ser = server.NearDBServer(seraddr, milvusHost, milvusPort, collection, kvdbpath)
ser.run()