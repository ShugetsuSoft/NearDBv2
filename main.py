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
else:
    milvusHost = "127.0.0.1"
    milvusPort = "19530"

ser = server.NearDBServer(seraddr, milvusHost, milvusPort)
ser.run()