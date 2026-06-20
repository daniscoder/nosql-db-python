import pytest
from engine.database import Database
from engine.query import QueryEngine


@pytest.fixture
def db():
    database = Database()
    database.create_collection("test")
    col = database.get_collection("test")
    col.add({"title": "tolerate it", "genre": "pop", "year": 2020})
    col.add({"title": "my tears ricochet", "genre": "pop", "year": 2020})
    col.add({"title": "the bolter", "genre": "rock", "year": 2024})
    return database


def test_create_collection(db):
    assert "test" in db.list_collections()


def test_drop_collection(db):
    db.create_collection("temp")
    db.drop_collection("temp")
    assert "temp" not in db.list_collections()


def test_add_and_get_document(db):
    col = db.get_collection("test")
    docs = col.get_all()
    assert len(docs) == 3


def test_get_document_by_uuid(db):
    col = db.get_collection("test")
    uuid = col.add({"title": "new doc"})
    doc = col.get(uuid)
    assert doc is not None
    assert doc["title"] == "new doc"


def test_update_document(db):
    col = db.get_collection("test")
    uuid = col.add({"title": "old title"})
    col.update(uuid, {"title": "new title"})
    doc = col.get(uuid)
    assert doc["title"] == "new title"


def test_delete_document(db):
    col = db.get_collection("test")
    uuid = col.add({"title": "to delete"})
    col.delete(uuid)
    assert col.get(uuid) is None


def test_query_contains(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"title": {"contains": "tears"}})
    assert len(results) == 1
    assert results[0]["title"] == "my tears ricochet"


def test_query_eq(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"genre": {"eq": "rock"}})
    assert len(results) == 1
    assert results[0]["title"] == "the bolter"


def test_query_starts_with(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"title": {"starts_with": "my"}})
    assert len(results) == 1


def test_query_gt(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"year": {"gt": 2020}})
    assert len(results) == 1
    assert results[0]["title"] == "the bolter"


def test_query_and(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({
        "and": [
            {"genre": {"eq": "pop"}},
            {"title": {"contains": "tolerate"}}
        ]
    })
    assert len(results) == 1
    assert results[0]["title"] == "tolerate it"


def test_query_or(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({
        "or": [
            {"genre": {"eq": "rock"}},
            {"title": {"contains": "tolerate"}}
        ]
    })
    assert len(results) == 2


def test_query_limit(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"genre": {"eq": "pop"}}, limit=1)
    assert len(results) == 1


def test_query_sort_by(db):
    col = db.get_collection("test")
    engine = QueryEngine(col)
    results = engine.search({"genre": {"eq": "pop"}}, sort_by="title")
    assert results[0]["title"] == "my tears ricochet"