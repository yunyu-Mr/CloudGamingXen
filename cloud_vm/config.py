# config paser
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("./server.conf")

servers = config.items("servers")
for key, server in servers:
    print key, server