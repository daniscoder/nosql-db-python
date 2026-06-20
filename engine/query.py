class QueryEngine:
    def __init__(self, collection):
        self.collection = collection

    def search(self, query: dict, limit: int | None = None, sort_by: str | None = None) -> list[dict]:
        documents = self.collection.get_all()
        results = self._evaluate(query, documents)

        if sort_by:
            results.sort(key=lambda d: d.get(sort_by, ""))

        if limit:
            results = results[:limit]

        return results

    def _evaluate(self, query: dict, documents: list[dict]) -> list[dict]:
        if "and" in query:
            sets = [set(d["uuid"] for d in self._evaluate(q, documents)) for q in query["and"]]
            uuids = set.intersection(*sets)
            return [d for d in documents if d["uuid"] in uuids]

        if "or" in query:
            sets = [set(d["uuid"] for d in self._evaluate(q, documents)) for q in query["or"]]
            uuids = set.union(*sets)
            return [d for d in documents if d["uuid"] in uuids]

        return self._apply_filter(query, documents)

    def _apply_filter(self, query: dict, documents: list[dict]) -> list[dict]:
        results = []
        for field, condition in query.items():
            operator, value = list(condition.items())[0]
            for doc in documents:
                doc_value = doc.get(field, "")
                if self._match(operator, doc_value, value):
                    results.append(doc)
        return results

    @staticmethod
    def _match(operator: str, doc_value, value) -> bool:
        doc_str = str(doc_value).lower()
        val_str = str(value).lower()

        if operator == "eq":
            return doc_str == val_str
        if operator == "contains":
            return val_str in doc_str
        if operator == "starts_with":
            return doc_str.startswith(val_str)
        if operator == "ends_with":
            return doc_str.endswith(val_str)
        if operator == "gt":
            return float(doc_value) > float(value)
        if operator == "lt":
            return float(doc_value) < float(value)
        return False