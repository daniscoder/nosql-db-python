from collections import defaultdict


class Index:
    def __init__(self, field: str):
        self.field = field
        self.data: dict[str, list[str]] = defaultdict(list)

    def add(self, uuid: str, value) -> None:
        key = str(value).lower()
        if uuid not in self.data[key]:
            self.data[key].append(uuid)

    def remove(self, uuid: str, value) -> None:
        key = str(value).lower()
        if uuid in self.data[key]:
            self.data[key].remove(uuid)
        if not self.data[key]:
            del self.data[key]

    def find(self, value) -> list[str]:
        key = str(value).lower()
        return self.data.get(key, [])

    def find_starts_with(self, prefix: str) -> list[str]:
        prefix = prefix.lower()
        result = []
        for key, uuids in self.data.items():
            if key.startswith(prefix):
                result.extend(uuids)
        return result

    def find_contains(self, substring: str) -> list[str]:
        substring = substring.lower()
        result = []
        for key, uuids in self.data.items():
            if substring in key:
                result.extend(uuids)
        return result