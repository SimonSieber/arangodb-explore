from database.accessor import ArangoAccessor
import database.schemas as schemas
import configuration
import nzn.collection_descriptions as desc


client = ArangoAccessor(
    db_name="NetZeroNet",
    host=configuration.ARANGO_HOST,
    username=configuration.ARANGO_USERNAME,
    password=configuration.ARANGO_PASSWORD,
)

nodes = [
    {"type": desc.NODE_COMPANY, "schema": schemas.NODE_COMPANY},
    {"type": desc.NODE_REPORT, "schema": schemas.NODE_REPORT},
    {"type": desc.NODE_NET_ZERO_TARGET, "schema": schemas.NODE_NET_ZERO_TARGET},
]
edges = [desc.REL_PUBLISHES, desc.REL_PUBLISHED_BY, desc.REL_DEFINED_IN, desc.REL_DEFINES]


if __name__ == "__main__":
    client.create_database()
    for node in nodes:
        client.create_collection(node["type"], schema=node.get("schema"))
    for edge in edges:
        client.create_collection(edge, edge=True)
