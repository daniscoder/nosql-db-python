# NoSQL Database in Python

[![Maintainability](https://qlty.sh/gh/daniscoder/projects/nosql-db-python/maintainability.svg)](https://qlty.sh/gh/daniscoder/projects/nosql-db-python)

A lightweight document-oriented NoSQL database built from scratch in Python.
Stores JSON documents, supports indexing and complex queries via REST API and Web UI.

## Stack

- Python 3.14
- Flask 3.1.3
- ujson
- pytest

## Features

- JSON document storage
- Collections management
- Query engine with filters: `eq`, `contains`, `starts_with`, `ends_with`, `gt`, `lt`
- Compound queries with `and` / `or` operators (including nested)
- Global Secondary Indexes (GSI)
- REST API (10 endpoints)
- Web UI — collection explorer with query console
- Unit tests (14 tests)

## Project structure

```
nosql-db-python/
├── engine/
│   ├── collection.py   # Collection management
│   ├── database.py     # Database class
│   ├── document.py     # Document model
│   ├── index.py        # GSI index
│   └── query.py        # Query engine
├── storage/
│   └── json_store.py   # JSON persistence layer
├── templates/
│   └── index.html      # Web UI
├── tests/
│   └── test_engine.py  # Unit tests
├── app.py              # Flask REST API
├── Procfile            # Render deploy config
└── requirements.txt
```

## Run locally

```bash
pip install -r requirements.txt
python app.py
```

## API

| Method | URL                      | Description          |
|--------|--------------------------|----------------------|
| GET    | /db/collections          | List collections     |
| POST   | /db/collections          | Create collection    |
| DELETE | /db/collections/{name}   | Drop collection      |
| POST   | /db/{col}/documents      | Add document         |
| GET    | /db/{col}/documents      | Get all documents    |
| GET    | /db/{col}/documents/{id} | Get document by UUID |
| PUT    | /db/{col}/documents/{id} | Update document      |
| DELETE | /db/{col}/documents/{id} | Delete document      |
| POST   | /db/{col}/query          | Query with filters   |
| POST   | /db/{col}/index          | Create index         |

## Deploy

https://nosql-db-python.onrender.com

## Source

Based on:
- Tutorial: https://jamesg.blog/2024/08/19/nosql-database-python
- Catalog: https://github.com/practical-tutorials/project-based-learning