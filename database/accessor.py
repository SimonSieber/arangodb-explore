from arango import ArangoClient


class ArangoAccessor:
    def __init__(self, db_name: str, host: str, username: str, password: str):
        self.db_name = db_name
        self.host = host
        self.username = username
        self.password = password
        self.client = ArangoClient(hosts=self.host)
        self.db = self.client.db(self.db_name, username=self.username, password=self.password)

    def create_database(self):
        sys_db = self.client.db("_system", username=self.username, password=self.password)
        sys_db.create_database(self.db_name)

    def create_collection(self, collection_name: str, edge: bool = False):
        return self.db.create_collection(collection_name, edge=edge)
