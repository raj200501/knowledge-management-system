# Knowledge Management System

A lightweight, runnable knowledge management system with a Python standard-library HTTP API, a small C-based system module, and supporting AI/ML and security utilities. The project ships with deterministic scripts to run and verify the system in a clean checkout.

> **Scope note**: The iOS application is included for reference only and is not validated in CI. The verified workflow focuses on the backend API, the core OS module, the AI/ML utilities, and the security/SRE utilities.

## Features

- **Backend API (Python + SQLite)**
  - CRUD for knowledge entries
  - Search, pagination, and health endpoint
- **Core OS Module (C)**
  - Secure file operation (XOR-based demo)
  - System monitoring with bounded iterations
- **AI/ML Utilities (pure Python)**
  - Data preprocessing
  - Naive Bayes text classification (train + inference)
- **Security & SRE Utilities**
  - PBKDF2 password hashing/verification
  - Lightweight system health report

## Repository Layout

```
backend/        Python HTTP API
core-os/        C module
ai-ml/          ML utilities and sample data
security/       Security and SRE utilities
web-app/        Static web UI (optional)
scripts/        Run and verification scripts
```

## Verified Quickstart (Backend API)

> These commands are **verified** and mirrored in `scripts/run.sh`.

```sh
./scripts/run.sh
```

The backend starts at `http://127.0.0.1:5000`.

### Example API calls

```sh
curl -s http://127.0.0.1:5000/health

curl -s -X POST http://127.0.0.1:5000/entry \
  -H 'Content-Type: application/json' \
  -d '{"title":"First Entry","content":"Hello knowledge base","tags":["intro","example"]}'

curl -s http://127.0.0.1:5000/entries?query=hello
```

## Verified Verification

> This command is **verified** and is also what CI runs.

```sh
./scripts/verify.sh
```

`verify.sh` performs:
- Unit tests (Python `unittest`)
- Core OS module build + runtime checks
- AI/ML train/infer checks
- Security and SRE CLI checks
- Integration smoke test against the running API

## Configuration

Defaults are safe, but can be overridden using environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `KMS_DB_URL` | `sqlite:///knowledge.db` | SQLite database URI |
| `KMS_ENV` | `development` | Runtime environment |
| `KMS_LOG_LEVEL` | `INFO` | Logging level |
| `KMS_PAGE_SIZE` | `20` | Default pagination size |
| `KMS_PORT` | `5000` | API port |

See `.env.example` for a sample.

## Dependencies

The verified workflow uses only the Python standard library and system tooling (`gcc` + `make`). No third-party Python packages are required.

## Optional: Web App

A simple static web app is provided. It expects the backend to be running on `http://127.0.0.1:5000`.

```sh
cd web-app
python3 -m http.server 3000
```

Then open `http://localhost:3000` in your browser.

## Optional: Core OS Module Manual Run

```sh
cd core-os
make
./core_os_module secure
./core_os_module monitor --iterations 2
```

## Optional: AI/ML Utilities

```sh
cd ai-ml
python3 data_preprocessing.py --input data/sample.csv --output artifacts/split.json
python3 training.py --input data/sample.csv --model artifacts/model.json
python3 llm.py --model artifacts/model.json --text "Example classification"
```

## Troubleshooting

- If `make` fails for the core OS module, ensure `gcc` is installed.
- If the API cannot bind to port 5000, set `KMS_PORT=5001` and retry.
- For a clean database, delete `backend/knowledge.db`.

## Contributing

See `docs/CONTRIBUTING.md`.
