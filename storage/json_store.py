from pathlib import Path
import ujson


class JsonStore:
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, collection_name: str) -> Path:
        return self.storage_dir / f"{collection_name}.json"

    def save(self, collection_name: str, documents: dict) -> None:
        self._path(collection_name).write_text(
            ujson.dumps(documents, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

    def load(self, collection_name: str) -> dict:
        path = self._path(collection_name)
        if not path.exists():
            return {}
        return ujson.loads(path.read_text(encoding="utf-8"))

    def delete(self, collection_name: str) -> bool:
        path = self._path(collection_name)
        if path.exists():
            path.unlink()
            return True
        return False

    def list_collections(self) -> list[str]:
        return [p.stem for p in self.storage_dir.glob("*.json")]