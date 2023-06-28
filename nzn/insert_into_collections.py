from ast import literal_eval
from pathlib import Path
import os

import pandas as pd

from database.accessor import ArangoAccessor
from database.models import Node, Relationship
import configuration
import nzn.collection_descriptions as desc

client = ArangoAccessor(
    db_name="NetZeroNet",
    host=configuration.ARANGO_HOST,
    username=configuration.ARANGO_USERNAME,
    password=configuration.ARANGO_PASSWORD,
)

FILE_PATH = Path("../data/")


def read_parse_company_nodes():
    df = pd.read_excel(os.path.join(FILE_PATH, "asset_owners_company.xlsx"), dtype=str)
    df["id"] = df["ownaha_company_id"]
    df = df.to_dict(orient="records")
    data = [Node(d).to_arango_document() for d in df]
    return data


def read_parse_reports():
    df = pd.read_excel(
        os.path.join(FILE_PATH, "reports.xlsx"),
        usecols=[
            "filename",
            "type",
            "publication_year",
            "report_year",
            "id",
        ],
        dtype=str,
    )
    df["type"] = df["type"].apply(literal_eval)
    df = df.to_dict(orient="records")
    data = [Node(d).to_arango_document() for d in df]
    return data


def read_parse_report_company_edges():
    df = pd.read_excel(
        os.path.join(FILE_PATH, "reports.xlsx"),
        usecols=["id", "ownaha_company_id"],
        dtype=str,
    )
    df = df.to_dict(orient="records")
    published_by = [
        Relationship(
            relationship_type=desc.REL_PUBLISHED_BY,
            from_node=dict(type=desc.NODE_REPORT, id=d["id"]),
            to_node=dict(type=desc.NODE_COMPANY, id=d["ownaha_company_id"]),
        ).to_arango_edge()
        for d in df
    ]
    publishes = [
        Relationship(
            relationship_type=desc.REL_PUBLISHES,
            from_node=dict(type=desc.NODE_COMPANY, id=d["ownaha_company_id"]),
            to_node=dict(type=desc.NODE_REPORT, id=d["id"]),
        ).to_arango_edge()
        for d in df
    ]
    result = {desc.REL_PUBLISHED_BY: published_by, desc.REL_PUBLISHES: publishes}
    return result


def read_parse_targets():
    df = pd.read_excel(
        os.path.join(FILE_PATH, "net_zero_targets.xlsx"),
        usecols=[
            "id",
            "target_year",
            "reference_year",
            "absolute_target_value",
            "relative_target_value",
            "company_division",
        ],
        dtype=str,
    )
    df = df.where(pd.notnull(df), None)
    df = df.to_dict(orient="records")
    data = [Node(d).to_arango_document() for d in df]
    return data


def read_parse_target_report_connection():
    df = pd.read_excel(
        os.path.join(FILE_PATH, "net_zero_targets.xlsx"),
        usecols=["page", "text", "statement", "id", "report_id"],
        dtype=str,
    )
    df["page"] = df["page"].astype(int)
    df = df.where(pd.notnull(df), None)
    df = df.to_dict(orient="records")
    defined_in = [
        Relationship(
            relationship_type=desc.REL_DEFINED_IN,
            from_node=dict(type=desc.NODE_NET_ZERO_TARGET, id=d["id"]),
            to_node=dict(type=desc.NODE_REPORT, id=d["report_id"]),
            properties=dict(page=d["page"], text=d["text"], statement=d["statement"]),
        ).to_arango_edge()
        for d in df
    ]
    defines = [
        Relationship(
            relationship_type=desc.REL_DEFINES,
            from_node=dict(type=desc.NODE_REPORT, id=d["report_id"]),
            to_node=dict(type=desc.NODE_NET_ZERO_TARGET, id=d["id"]),
            properties=dict(page=d["page"], text=d["text"], statement=d["statement"]),
        ).to_arango_edge()
        for d in df
    ]
    result = {desc.REL_DEFINED_IN: defined_in, desc.REL_DEFINES: defines}
    return result


def create_graph():
    # desc.REL_DEFINED_IN, desc.REL_DEFINES
    edge_definitions = [
        {
            "edge_collection": desc.REL_PUBLISHES,
            "from_vertex_collections": [desc.NODE_COMPANY],
            "to_vertex_collections": [desc.NODE_REPORT],
        },
        {
            "edge_collection": desc.REL_PUBLISHED_BY,
            "from_vertex_collections": [desc.NODE_REPORT],
            "to_vertex_collections": [desc.NODE_COMPANY],
        },
        {
            "edge_collection": desc.REL_DEFINED_IN,
            "from_vertex_collections": [desc.NODE_NET_ZERO_TARGET],
            "to_vertex_collections": [desc.NODE_REPORT],
        },
        {
            "edge_collection": desc.REL_DEFINES,
            "from_vertex_collections": [desc.NODE_REPORT],
            "to_vertex_collections": [desc.NODE_NET_ZERO_TARGET],
        },
    ]
    client.db.create_graph(name="graph", edge_definitions=edge_definitions)


def main():
    # insert nodes
    client.insert_into_collection(desc.NODE_COMPANY, read_parse_company_nodes())
    client.insert_into_collection(desc.NODE_REPORT, read_parse_reports())
    client.insert_into_collection(desc.NODE_NET_ZERO_TARGET, read_parse_targets())

    # read edges
    rel_publish = read_parse_report_company_edges()
    rel_defines = read_parse_target_report_connection()

    # insert edges
    client.insert_into_collection(desc.REL_PUBLISHED_BY, rel_publish[desc.REL_PUBLISHED_BY])
    client.insert_into_collection(desc.REL_PUBLISHES, rel_publish[desc.REL_PUBLISHES])
    client.insert_into_collection(desc.REL_DEFINES, rel_defines[desc.REL_DEFINES])
    client.insert_into_collection(desc.REL_DEFINED_IN, rel_defines[desc.REL_DEFINED_IN])

    # create graph
    create_graph()


if __name__ == "__main__":
    main()
