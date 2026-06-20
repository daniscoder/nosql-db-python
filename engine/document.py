import uuid


class Document:
    def __init__(self, data: dict):
        self.uuid = str(uuid.uuid4())
        self.data = data

    def to_dict(self) -> dict:
        return {"uuid": self.uuid, **self.data}

    @classmethod
    def from_dict(cls, data: dict) -> "Document":
        doc = cls.__new__(cls)
        doc.uuid = data.pop("uuid")
        doc.data = data
        return doc