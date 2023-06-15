import os
from pathlib import Path

from arango import ArangoClient
from tqdm import tqdm

from wikidata.parser import WikidataParser


parser = WikidataParser()

WORKING_DB = "NetZeroNet"
client = ArangoClient(hosts="http://localhost:8529")


def get_db(db_name: str):
    return client.db(db_name, username="root", password="example")


db = get_db("NetZeroNet")


def accessor_insert(file):
    entity = parser(file)

    node = entity["source_node"].to_arango_document()
    relationships = [x.to_arango_edge() for x in entity["relations"]]

    db.collection("Entities").insert(node, overwrite_mode="replace")

    for relationship in relationships:
        db.collection(relationship["id"]).insert(relationship, overwrite_mode="replace")


def insert_items():
    SOURCE_PATH = Path(os.path.join(Path().home(), "Documents/wikidata_sp500_entities_json"))
    SOURCE_FILES = sorted(list(SOURCE_PATH.glob("*.json")))
    # files = [Path(os.path.join(Path().home(), "Documents/wikidata_sp500_entities_json/Q1.json"))]
    for file in tqdm(SOURCE_FILES):
        accessor_insert(file)
