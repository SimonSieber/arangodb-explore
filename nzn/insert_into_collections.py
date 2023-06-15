from typing import List

from arango import ArangoClient

from nzn.parse_files import read_pension_funds

WORKING_DB = "NetZeroNet"
client = ArangoClient(hosts="http://localhost:8529")


def get_db(db_name: str):
    return client.db(db_name, username="root", password="example")


db = get_db("NetZeroNet")


def accessor_insert(nodes: List[dict], collection):
    db.collection(collection).insert_many(nodes, overwrite_mode="replace")


accessor_insert(read_pension_funds(), "pension_fund")
