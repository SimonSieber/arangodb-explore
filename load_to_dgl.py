from arango import ArangoClient

from adbdgl_adapter import ADBDGL_Adapter


# TODO: newest version of library 'dgl' will fail, now version 0.6.1 is used (dgl==0.6.1)
client = ArangoClient(hosts="http://localhost:8529")
db = client.db("NetZeroNet", username="root", password="example")

adbdgl_adapter = ADBDGL_Adapter(db)

graph = adbdgl_adapter.arangodb_graph_to_dgl("graph")
