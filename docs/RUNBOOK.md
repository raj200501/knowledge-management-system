# Runbook

## Health Checks

- `GET /health` for API status
- `python3 security/sre.py report` for host-level uptime output

## Routine Maintenance

- Rotate the SQLite database by archiving `backend/knowledge.db`.
- Keep `ai-ml/artifacts/` clean to avoid stale models.

## Incident Response Checklist

1. Verify API health with `curl -s http://127.0.0.1:5000/health`.
2. Inspect logs from the running Flask process.
3. Check system health with `python3 security/sre.py report`.
4. Validate the core OS module: `cd core-os && ./core_os_module monitor --iterations 1`.
