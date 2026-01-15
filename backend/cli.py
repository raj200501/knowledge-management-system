import argparse
import json

from backend.config import config
from backend.database import init_db
from backend.utils import format_response


def main():
    parser = argparse.ArgumentParser(description="Knowledge Management System CLI")
    parser.add_argument("command", choices=["init-db", "health"], help="Command to run")
    args = parser.parse_args()

    if args.command == "init-db":
        init_db()
        print("Database initialized at", config.DB_URL)
        return 0
    if args.command == "health":
        payload = format_response(
            {
                "status": "ok",
                "environment": config.ENV,
                "page_size": config.PAGE_SIZE,
            }
        )
        print(json.dumps(payload, indent=2))
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
