import pandas as pd
from tqdm import tqdm

import configuration
from database.accessor import ArangoAccessor


client = ArangoAccessor(
    db_name="wikidata",
    host=configuration.ARANGO_HOST,
    username=configuration.ARANGO_USERNAME,
    password=configuration.ARANGO_PASSWORD,
)


def read_rel_prop_labels():
    df = pd.read_csv("all_properties.csv")
    df = df[df["propertyTypeLabel"] == "http://wikiba.se/ontology#WikibaseItem"].copy()
    df["property"] = df["property"].str.split("/").str[-1]
    result = df["property"].tolist()
    return result


def create_collections():
    props = read_rel_prop_labels()
    client.create_collection("Entities")
    for prop in tqdm(props):
        client.create_collection(prop, edge=True)


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
    client.db.create_graph(name="graph_all_relations", edge_definitions=edge_definitions)


if __name__ == "__main__":
    client.create_database()
    create_collections()
    create_graph()
