import os
from pathlib import Path

from tqdm import tqdm

import configuration
from wikidata.parser import WikidataParser
from database.accessor import ArangoAccessor


parser = WikidataParser()
client = ArangoAccessor(
    db_name="wikidata",
    host=configuration.ARANGO_HOST,
    username=configuration.ARANGO_USERNAME,
    password=configuration.ARANGO_PASSWORD,
)


def accessor_insert(file):
    entity = parser(file)

    node = entity["source_node"].to_arango_document()
    relationships = [x.to_arango_edge() for x in entity["relations"]]

    client.db.collection("Entities").insert(node, overwrite_mode="replace")

    for relationship in relationships:
        client.db.collection(relationship["id"]).insert(relationship, overwrite_mode="replace")


def insert_items():
    source_path = Path(os.path.join(Path().home(), "Documents/wikidata_sp500_entities_json"))
    source_files = sorted(list(source_path.glob("*.json")))
    for file in tqdm(source_files):
        accessor_insert(file)


if __name__ == "__main__":
    insert_items()
