class Node:
    key: str = None

    def __init__(self, properties: dict):
        self.properties = properties
        self.key = str(properties["id"])

    def to_arango_document(self):
        document = self.properties.copy()
        document["_key"] = self.key
        return document


class Relationship:
    def __init__(self, relationship_type, properties, from_node, to_node):
        self.relationship_type = relationship_type
        self.properties = properties
        self.from_node = from_node
        self.to_node = to_node

    def to_arango_edge(self):
        edge = self.properties.copy()
        edge["_key"] = f"{self.from_node}-{self.relationship_type}-{self.to_node}"
        edge["_from"] = f"Entities/{self.from_node}"
        edge["_to"] = f"Entities/{self.to_node}"
        return edge
