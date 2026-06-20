from flask import Flask, request, jsonify, render_template
from engine.database import Database
from engine.document import Document
from engine.query import QueryEngine
from storage.json_store import JsonStore

app = Flask(__name__)
db = Database()
store = JsonStore()


def restore_from_disk() -> None:
    for saved_name in store.list_collections():
        db.create_collection(saved_name)
        saved = store.load(saved_name)
        col = db.get_collection(saved_name)
        if col is None:
            continue
        for saved_uuid, saved_data in saved.items():
            restored = object.__new__(Document)
            restored.uuid = saved_uuid
            restored.data = saved_data
            col.documents[saved_uuid] = restored


restore_from_disk()


@app.route("/")
def index():
    return render_template("index.html")


# — Collections —

@app.route("/db/collections", methods=["GET"])
def list_collections():
    return jsonify({"collections": db.list_collections()})


@app.route("/db/collections", methods=["POST"])
def create_collection():
    collection_name = request.json.get("name")
    if not collection_name:
        return jsonify({"error": "name is required"}), 400
    if not db.create_collection(collection_name):
        return jsonify({"error": "collection already exists"}), 409
    return jsonify({"status": "created", "name": collection_name}), 201


@app.route("/db/collections/<collection_name>", methods=["DELETE"])
def drop_collection(collection_name):
    if not db.drop_collection(collection_name):
        return jsonify({"error": "collection not found"}), 404
    store.delete(collection_name)
    return jsonify({"status": "deleted", "name": collection_name})


# — Documents —

@app.route("/db/<collection_name>/documents", methods=["POST"])
def add_document(collection_name):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    doc_uuid = collection.add(request.json)
    store.save(collection_name, {u: d.data for u, d in collection.documents.items()})
    return jsonify({"uuid": doc_uuid}), 201


@app.route("/db/<collection_name>/documents", methods=["GET"])
def get_documents(collection_name):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    return jsonify({"documents": collection.get_all()})


@app.route("/db/<collection_name>/documents/<doc_uuid>", methods=["GET"])
def get_document(collection_name, doc_uuid):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    doc = collection.get(doc_uuid)
    if not doc:
        return jsonify({"error": "document not found"}), 404
    return jsonify(doc)


@app.route("/db/<collection_name>/documents/<doc_uuid>", methods=["PUT"])
def update_document(collection_name, doc_uuid):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    if not collection.update(doc_uuid, request.json):
        return jsonify({"error": "document not found"}), 404
    store.save(collection_name, {u: d.data for u, d in collection.documents.items()})
    return jsonify({"status": "updated", "uuid": doc_uuid})


@app.route("/db/<collection_name>/documents/<doc_uuid>", methods=["DELETE"])
def delete_document(collection_name, doc_uuid):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    if not collection.delete(doc_uuid):
        return jsonify({"error": "document not found"}), 404
    store.save(collection_name, {u: d.data for u, d in collection.documents.items()})
    return jsonify({"status": "deleted", "uuid": doc_uuid})


# — Query —

@app.route("/db/<collection_name>/query", methods=["POST"])
def query_documents(collection_name):
    collection = db.get_collection(collection_name)
    if not collection:
        return jsonify({"error": "collection not found"}), 404
    body = request.json
    engine = QueryEngine(collection)
    results = engine.search(
        query=body.get("query", {}),
        limit=body.get("limit"),
        sort_by=body.get("sort_by")
    )
    return jsonify({"documents": results, "count": len(results)})


if __name__ == "__main__":
    app.run(debug=True)