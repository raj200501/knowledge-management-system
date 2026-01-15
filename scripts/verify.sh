#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PORT=$(python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
)

export KMS_PORT="$PORT"

python3 -m unittest discover -s "$ROOT_DIR/backend/tests" -p "test_*.py"
python3 -m unittest discover -s "$ROOT_DIR/ai-ml/tests" -p "test_*.py"

pushd "$ROOT_DIR/core-os" >/dev/null
make clean
make
./core_os_module secure
./core_os_module monitor --iterations 2 --interval 1
popd >/dev/null

python3 "$ROOT_DIR/ai-ml/data_preprocessing.py" --input "$ROOT_DIR/ai-ml/data/sample.csv" --output "$ROOT_DIR/ai-ml/artifacts/split.json"
python3 "$ROOT_DIR/ai-ml/training.py" --input "$ROOT_DIR/ai-ml/data/sample.csv" --model "$ROOT_DIR/ai-ml/artifacts/model.json"
python3 "$ROOT_DIR/ai-ml/llm.py" --model "$ROOT_DIR/ai-ml/artifacts/model.json" --text "Example classification"

SECURITY_HASH_OUTPUT=$(python3 "$ROOT_DIR/security/security.py" hash --password "example")
SALT=$(echo "$SECURITY_HASH_OUTPUT" | awk -F= '/salt=/{print $2}')
HASH=$(echo "$SECURITY_HASH_OUTPUT" | awk -F= '/hash=/{print $2}')
python3 "$ROOT_DIR/security/security.py" verify --password "example" --salt "$SALT" --hash "$HASH"
python3 "$ROOT_DIR/security/sre.py" report

python3 -m backend.app >/dev/null 2>&1 &
APP_PID=$!

cleanup() {
  kill "$APP_PID" || true
}
trap cleanup EXIT

for _ in {1..10}; do
  if curl -s "http://127.0.0.1:$PORT/health" >/dev/null; then
    break
  fi
  sleep 0.5
done

curl -s http://127.0.0.1:$PORT/health | grep -q '"status"'

CREATE_RESPONSE=$(curl -s -X POST http://127.0.0.1:$PORT/entry \
  -H 'Content-Type: application/json' \
  -d '{"title":"Verify Entry","content":"Verify content here","tags":["verify","smoke"]}')

ENTRY_ID=$(echo "$CREATE_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['data']['id'])")

curl -s http://127.0.0.1:$PORT/entry/$ENTRY_ID | grep -q 'Verify Entry'
curl -s http://127.0.0.1:$PORT/entries?query=Verify | grep -q 'Verify Entry'

curl -s -X DELETE http://127.0.0.1:$PORT/entry/$ENTRY_ID | grep -q 'Entry deleted'
