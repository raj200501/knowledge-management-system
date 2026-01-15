# Usage Guide

## Backend API

The backend server runs on `http://127.0.0.1:5000` by default and uses the Python standard library.

### Endpoints

- `GET /health`: Health check with service metadata.
- `GET /entries`: Retrieve knowledge entries with pagination and search.
  - Query params: `query`, `tag`, `limit`, `offset`
- `POST /entry`: Add a new knowledge entry.
- `GET /entry/<id>`: Retrieve a specific knowledge entry by ID.
- `PUT /entry/<id>`: Update a knowledge entry by ID.
- `DELETE /entry/<id>`: Delete a knowledge entry by ID.

### Example Workflow

```sh
curl -s http://127.0.0.1:5000/health

curl -s -X POST http://127.0.0.1:5000/entry \
  -H 'Content-Type: application/json' \
  -d '{"title":"First Entry","content":"Hello knowledge base","tags":["intro","example"]}'

curl -s http://127.0.0.1:5000/entries?query=hello
```

## Web App

The web app is static and expects the backend running at `http://127.0.0.1:5000`.

```sh
cd web-app
python3 -m http.server 3000
```

Then open `http://localhost:3000`.

## AI/ML Utilities

The AI/ML utilities are designed to be run locally with the sample dataset.

```sh
cd ai-ml
python3 data_preprocessing.py --input data/sample.csv --output artifacts/split.json
python3 training.py --input data/sample.csv --model artifacts/model.json
python3 llm.py --model artifacts/model.json --text "Example classification"
```

## Security and SRE

```sh
cd security
python3 security.py hash --password "example"
python3 security.py verify --password "example" --hash <hash> --salt <salt>
python3 sre.py report
```
