from arango import ArangoClient
import pandas as pd
from tqdm import tqdm


WORKING_DB = "NetZeroNet"
client = ArangoClient(hosts="http://localhost:8529")
DB = client.db(WORKING_DB, username="root", password="example")


def create_database():
    sys_db = client.db("_system", username="root", password="example")
    sys_db.create_database(WORKING_DB)


def get_db(db_name: str):
    return client.db(db_name, username="root", password="example")


def create_collection(coll_name: str, edge=False):
    DB.create_collection(coll_name, edge=edge)


def read_rel_prop_labels():
    df = pd.read_csv("all_properties.csv")
    df = df[df["propertyTypeLabel"] == "http://wikiba.se/ontology#WikibaseItem"].copy()
    df["property"] = df["property"].str.split("/").str[-1]
    result = df["property"].tolist()
    return result


def create_collections():
    props = read_rel_prop_labels()
    create_collection("Entities")
    for prop in tqdm(props):
        create_collection(prop, edge=True)


def create_graph():
    props = read_rel_prop_labels()
    edge_definitions = [
        {
            "edge_collection": prop,
            "from_vertex_collections": ["Entities"],
            "to_vertex_collections": ["Entities"],
        }
        for prop in props
    ]
    DB.create_graph(name="graph_all_relations", edge_definitions=edge_definitions)
