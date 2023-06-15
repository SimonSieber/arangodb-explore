from datetime import datetime
from pathlib import Path
from typing import Generator
import json
import os

from database.models import Node, Relationship

# TODO: add datatypes into json
class WikidataParser:
    def __init__(self):
        self.rel_prop_labels = self.read_rel_prop_labels()

    @staticmethod
    def read_rel_prop_labels():
        path = Path(
            os.path.join(
                Path().home(),
                "PycharmProjects/wikidata-neo4j/wikidata/all_properties.json",
            )
        )
        with open(path, "r") as fp:
            items = json.load(fp)
        result = {x["property"].split("/")[-1]: x["propertyLabel"] for x in items}
        return result

    @staticmethod
    def unpack_entity(ent: dict) -> dict:
        return ent["entities"][next(iter(ent["entities"]))]

    @staticmethod
    def load_json(file: str) -> dict:
        with open(file, "r") as fp:
            item = json.load(fp)
            return item

    @staticmethod
    def concat_claims(claims: dict) -> Generator:
        for _, rel_claims in claims.items():
            for claim in rel_claims:
                yield claim

    @staticmethod
    def concat_labels(labels: dict) -> dict:
        return {key: labels[key]["value"] for key in labels.keys()}

    @staticmethod
    def concat_sitelinks(sitelinks: dict) -> dict:
        return {key: sitelinks[key]["url"] for key in sitelinks.keys()}

    @staticmethod
    def concat_aliases(aliases: dict) -> dict:
        flatted_aliases = {key: [x["value"] for x in aliases[key]] for key in aliases.keys()}
        return flatted_aliases

    @staticmethod
    def concat_descriptions(descriptions: dict) -> dict:
        return {key: descriptions[key]["value"] for key in descriptions.keys()}

    @staticmethod
    def parse_datatype(item: dict) -> dict:
        value_type = item["type"]
        parsed_values = {}
        if value_type == "time":
            try:
                if item["value"]["precision"] >= 11:
                    if item["value"]["time"][0] == "-":
                        raise ValueError
                    new_time = datetime.fromisoformat(item["value"]["time"][1:-1]).isoformat()
                elif item["value"]["precision"] == 10:
                    new_time = datetime(
                        year=int(item["value"]["time"][:5]),
                        month=int(item["value"]["time"][6:8]),
                        day=1,
                    ).isoformat()
                else:
                    new_time = datetime(year=int(item["value"]["time"][:5]), month=1, day=1).isoformat()
            except ValueError:
                new_time = item["value"]["time"]
            parsed_values["value"] = new_time
        elif value_type in "string":
            parsed_values["value"] = item["value"]
        elif value_type == "monolingualtext":
            parsed_values["value"] = item["value"]["text"]
        elif value_type == "quantity":
            temp_value = item["value"]["amount"][1:]
            parsed_values["value"] = float(temp_value) if "." in temp_value else int(temp_value)
        elif value_type == "globecoordinate":
            parsed_values["latitude"] = float(item["value"]["latitude"])
            parsed_values["longitude"] = float(item["value"]["longitude"])
        parsed_values["type"] = value_type
        return parsed_values

    def parse_qualifiers(self, qualifiers: dict) -> dict:
        parsed_qualifiers = {}
        for key in qualifiers.keys():
            if qualifiers[key][0]["snaktype"] != "value":
                continue
            item = qualifiers[key][0]["datavalue"]
            temp_qualifiers = self.parse_datatype(item)
            if temp_qualifiers:
                parsed_qualifiers[key] = temp_qualifiers

        return parsed_qualifiers

    def to_triplets(self, ent) -> dict:
        labels = {"labels": self.concat_labels(ent["labels"])}
        aliases = {"aliases": self.concat_aliases(ent["aliases"])}
        descriptions = {"descriptions": self.concat_descriptions(ent["descriptions"])}
        sitelinks = {"sitelinks": self.concat_sitelinks(ent["sitelinks"])}
        node_props = {"id": ent["id"]}
        node_props = {**node_props, **labels, **aliases, **descriptions, **sitelinks}
        rels = []
        from_node = Node({"id": ent["id"]})

        claims = self.concat_claims(ent["claims"])
        claim_node_props = {}

        for claim in claims:
            mainsnak = claim["mainsnak"]
            rel = mainsnak["property"]

            if mainsnak["snaktype"] != "value":
                continue
            elif mainsnak["datatype"] == "wikibase-item":
                rel_qualifiers = self.parse_qualifiers(claim.get("qualifiers", {}))
                rel_rank = claim.get("rank", None)
                rel_rank = {"rank": rel_rank} if rel_rank else {}
                rel_props = {"label": self.rel_prop_labels.get(rel, ""), "id": rel}
                rel_props = {**rel_props, **rel_qualifiers, **rel_rank}

                to_node = Node({"id": f"Q{mainsnak['datavalue']['value']['numeric-id']}"})
                relationship = Relationship(rel, rel_props, from_node.key, to_node.key)
                rels.append(relationship)
            else:
                temp_node_props = self.parse_datatype(mainsnak["datavalue"])
                node_qualifiers = self.parse_qualifiers(claim.get("qualifiers", {}))
                node_qualifiers = {key: node_qualifiers[key] for key in node_qualifiers.keys()}
                node_rank = claim.get("rank", None)
                claim_node_prop = {rel: [temp_node_props]}

                if node_qualifiers:
                    claim_node_prop[rel][0]["qualifiers"] = node_qualifiers
                if node_rank:
                    claim_node_prop[rel][0]["rank"] = node_rank

                if rel in claim_node_props:
                    claim_node_props[rel] += claim_node_prop[rel]
                else:
                    claim_node_props[rel] = claim_node_prop[rel]

        node_props = {**node_props, **claim_node_props}
        item = {
            "source_node": Node(node_props),
            "relations": rels,
        }
        return item

    def __call__(self, filename):
        payload = self.load_json(filename)
        entity = self.unpack_entity(payload)
        entity = self.to_triplets(entity)
        return entity
