# Troubleshooting

## Flask server fails to start

- Ensure Python 3.10+ is installed.
- Delete the local database: `rm backend/knowledge.db`.
- Check port availability: set `KMS_PORT=5001` to change ports.

## Core OS module build errors

- Install `gcc` and `make`.
- Run `make clean` and then `make`.

## AI/ML utilities fail

- Ensure the sample dataset exists at `ai-ml/data/sample.csv`.
- Delete old model artifacts before retraining: `rm ai-ml/artifacts/*.json`.

## Verification failures

- Always run `./scripts/verify.sh` from the repo root.
- Ensure you are not running another process on port 5000.
