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
    def __init__(
        self,
        relationship_type: str,
        from_node: dict,
        to_node: dict,
        properties: dict = None,
    ):
        self.relationship_type = relationship_type
        self.properties = properties if properties else {}
        self.from_node = from_node
        self.to_node = to_node

    def to_arango_edge(self):
        edge = self.properties.copy()
        edge["_key"] = f"{self.from_node['id']}-{self.relationship_type}-{self.to_node['id']}"
        edge["_from"] = f"{self.from_node['type']}/{self.from_node['id']}"
        edge["_to"] = f"{self.to_node['type']}/{self.to_node['id']}"
        return edge
