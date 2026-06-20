from engine.document import Document


class Collection:
    def __init__(self, name: str):
        self.name = name
        self.documents: dict[str, Document] = {}

    def add(self, data: dict) -> str:
        doc = Document(data)
        self.documents[doc.uuid] = doc
        return doc.uuid

    def get(self, uuid: str) -> dict | None:
        doc = self.documents.get(uuid)
        return doc.to_dict() if doc else None

    def get_all(self) -> list[dict]:
        return [doc.to_dict() for doc in self.documents.values()]

    def delete(self, uuid: str) -> bool:
        if uuid in self.documents:
            del self.documents[uuid]
            return True
        return False

    def update(self, uuid: str, data: dict) -> bool:
        if uuid in self.documents:
            self.documents[uuid].data = data
            return True
        return False