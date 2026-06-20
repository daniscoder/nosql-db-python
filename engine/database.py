from engine.collection import Collection


class Database:
    def __init__(self):
        self.collections: dict[str, Collection] = {}

    def create_collection(self, name: str) -> bool:
        if name in self.collections:
            return False
        self.collections[name] = Collection(name)
        return True

    def get_collection(self, name: str) -> Collection | None:
        return self.collections.get(name)

    def drop_collection(self, name: str) -> bool:
        if name in self.collections:
            del self.collections[name]
            return True
        return False

    def list_collections(self) -> list[str]:
        return list(self.collections.keys())