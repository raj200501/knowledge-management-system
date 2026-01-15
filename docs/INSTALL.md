# Installation Guide

The verified workflow uses only the Python standard library and system tools. No external Python dependencies are required.

## Prerequisites

- Python 3.10+
- `gcc` and `make` for the C module

## Backend + Tooling (Verified)

```sh
./scripts/run.sh
```

`run.sh` launches the backend API using the system Python.

## Manual Setup (Optional)

```sh
python3 -m backend.app
```

## Core OS Module (Optional)

```sh
cd core-os
make
./core_os_module secure
```

## AI/ML Utilities (Optional)

```sh
cd ai-ml
python3 data_preprocessing.py --input data/sample.csv --output artifacts/split.json
python3 training.py --input data/sample.csv --model artifacts/model.json
python3 llm.py --model artifacts/model.json --text "Example classification"
```

## Web App (Optional)

```sh
cd web-app
python3 -m http.server 3000
```

Then open `http://localhost:3000`.
