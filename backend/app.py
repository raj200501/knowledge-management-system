import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

from backend.config import config
from backend.database import (
    init_db,
    create_entry,
    get_entry,
    update_entry,
    delete_entry,
    list_entries,
)
from backend.utils import (
    format_response,
    format_error,
    normalize_tags,
    validate_entry_payload,
    sanitize_query,
    parse_pagination,
)


def _parse_json_body(request_handler):
    content_length = int(request_handler.headers.get("Content-Length", 0))
    if content_length == 0:
        return None
    raw_body = request_handler.rfile.read(content_length)
    try:
        return json.loads(raw_body)
    except json.JSONDecodeError:
        return None


class KnowledgeHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _not_found(self):
        payload, status = format_error("Not found", 404)
        self._send_json(status, payload)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query_params = parse_qs(parsed.query)

        if path == "/health":
            payload = format_response(
                {
                    "status": "ok",
                    "environment": config.ENV,
                    "page_size": config.PAGE_SIZE,
                }
            )
            self._send_json(200, payload)
            return

        if path == "/entries":
            query = sanitize_query(query_params.get("query", [None])[0])
            tag = query_params.get("tag", [None])[0]
            limit, offset = parse_pagination(query_params, config.PAGE_SIZE)
            total, entries = list_entries(query=query, tag=tag, limit=limit, offset=offset)
            payload = format_response(
                {
                    "items": entries,
                    "total": total,
                    "limit": limit,
                    "offset": offset,
                }
            )
            self._send_json(200, payload)
            return

        if path.startswith("/entry/"):
            try:
                entry_id = int(path.split("/")[2])
            except (IndexError, ValueError):
                payload, status = format_error("Invalid entry id", 400)
                self._send_json(status, payload)
                return

            entry = get_entry(entry_id)
            if entry is None:
                payload, status = format_error("Entry not found", 404)
                self._send_json(status, payload)
                return

            self._send_json(200, format_response(entry))
            return

        self._not_found()

    def do_POST(self):
        if self.path != "/entry":
            self._not_found()
            return

        payload = _parse_json_body(self)
        valid, message = validate_entry_payload(payload)
        if not valid:
            error_payload, status = format_error(message, 400)
            self._send_json(status, error_payload)
            return

        payload["tags"] = normalize_tags(payload.get("tags"))
        entry = create_entry(payload)
        self._send_json(201, format_response(entry))

    def do_PUT(self):
        if not self.path.startswith("/entry/"):
            self._not_found()
            return

        payload = _parse_json_body(self)
        valid, message = validate_entry_payload(payload, partial=True)
        if not valid:
            error_payload, status = format_error(message, 400)
            self._send_json(status, error_payload)
            return

        try:
            entry_id = int(self.path.split("/")[2])
        except (IndexError, ValueError):
            payload, status = format_error("Invalid entry id", 400)
            self._send_json(status, payload)
            return

        entry = get_entry(entry_id)
        if entry is None:
            payload, status = format_error("Entry not found", 404)
            self._send_json(status, payload)
            return

        updated_payload = {
            "title": payload.get("title", entry["title"]),
            "content": payload.get("content", entry["content"]),
            "tags": normalize_tags(payload.get("tags", entry["tags"])),
            "source": payload.get("source", entry["source"]),
            "status": payload.get("status", entry["status"]),
        }
        entry = update_entry(entry_id, updated_payload)
        self._send_json(200, format_response(entry))

    def do_DELETE(self):
        if not self.path.startswith("/entry/"):
            self._not_found()
            return

        try:
            entry_id = int(self.path.split("/")[2])
        except (IndexError, ValueError):
            payload, status = format_error("Invalid entry id", 400)
            self._send_json(status, payload)
            return

        if delete_entry(entry_id):
            self._send_json(200, format_response({"message": "Entry deleted"}))
            return

        payload, status = format_error("Entry not found", 404)
        self._send_json(status, payload)


class KnowledgeServer:
    def __init__(self, host="127.0.0.1", port=5000):
        self.server = HTTPServer((host, port), KnowledgeHandler)
        self.port = self.server.server_address[1]

    def serve(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()
        self.server.server_close()


def main():
    logging.basicConfig(level=config.LOG_LEVEL)
    init_db()
    server = KnowledgeServer(host="127.0.0.1", port=config.PORT)
    print(f"Knowledge API running on http://127.0.0.1:{server.port}")
    try:
        server.serve()
    except KeyboardInterrupt:
        print("Shutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
