import json
import os
import tempfile
import threading
import time
import unittest
import urllib.request

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in os.sys.path:
    os.sys.path.insert(0, ROOT)

from backend.app import KnowledgeServer
from backend.database import init_db


def _request(method, url, payload=None):
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        return resp.status, json.loads(body)


class BulkEntriesTestCase(unittest.TestCase):
    def setUp(self):
        fd, self.db_path = tempfile.mkstemp()
        os.close(fd)
        os.environ["KMS_DB_URL"] = f"sqlite:///{self.db_path}"
        init_db()
        self.server = KnowledgeServer(host="127.0.0.1", port=0)
        self.base_url = f"http://127.0.0.1:{self.server.port}"
        self.thread = threading.Thread(target=self.server.serve, daemon=True)
        self.thread.start()
        time.sleep(0.2)

    def tearDown(self):
        self.server.shutdown()
        os.unlink(self.db_path)

    def test_bulk_create_and_query(self):
        sample_entries = [
            {"title": "Entry 1", "content": "Content for entry 1", "tags": ["tag1", "tag1"]},
            {"title": "Entry 2", "content": "Content for entry 2", "tags": ["tag2", "tag2"]},
            {"title": "Entry 3", "content": "Content for entry 3", "tags": ["tag0", "tag3"]},
            {"title": "Entry 4", "content": "Content for entry 4", "tags": ["tag1", "tag4"]},
            {"title": "Entry 5", "content": "Content for entry 5", "tags": ["tag2", "tag0"]},
            {"title": "Entry 6", "content": "Content for entry 6", "tags": ["tag0", "tag1"]},
            {"title": "Entry 7", "content": "Content for entry 7", "tags": ["tag1", "tag2"]},
            {"title": "Entry 8", "content": "Content for entry 8", "tags": ["tag2", "tag3"]},
            {"title": "Entry 9", "content": "Content for entry 9", "tags": ["tag0", "tag4"]},
            {"title": "Entry 10", "content": "Content for entry 10", "tags": ["tag1", "tag0"]},
            {"title": "Entry 11", "content": "Content for entry 11", "tags": ["tag2", "tag1"]},
            {"title": "Entry 12", "content": "Content for entry 12", "tags": ["tag0", "tag2"]},
            {"title": "Entry 13", "content": "Content for entry 13", "tags": ["tag1", "tag3"]},
            {"title": "Entry 14", "content": "Content for entry 14", "tags": ["tag2", "tag4"]},
            {"title": "Entry 15", "content": "Content for entry 15", "tags": ["tag0", "tag0"]},
            {"title": "Entry 16", "content": "Content for entry 16", "tags": ["tag1", "tag1"]},
            {"title": "Entry 17", "content": "Content for entry 17", "tags": ["tag2", "tag2"]},
            {"title": "Entry 18", "content": "Content for entry 18", "tags": ["tag0", "tag3"]},
            {"title": "Entry 19", "content": "Content for entry 19", "tags": ["tag1", "tag4"]},
            {"title": "Entry 20", "content": "Content for entry 20", "tags": ["tag2", "tag0"]},
            {"title": "Entry 21", "content": "Content for entry 21", "tags": ["tag0", "tag1"]},
            {"title": "Entry 22", "content": "Content for entry 22", "tags": ["tag1", "tag2"]},
            {"title": "Entry 23", "content": "Content for entry 23", "tags": ["tag2", "tag3"]},
            {"title": "Entry 24", "content": "Content for entry 24", "tags": ["tag0", "tag4"]},
            {"title": "Entry 25", "content": "Content for entry 25", "tags": ["tag1", "tag0"]},
            {"title": "Entry 26", "content": "Content for entry 26", "tags": ["tag2", "tag1"]},
            {"title": "Entry 27", "content": "Content for entry 27", "tags": ["tag0", "tag2"]},
            {"title": "Entry 28", "content": "Content for entry 28", "tags": ["tag1", "tag3"]},
            {"title": "Entry 29", "content": "Content for entry 29", "tags": ["tag2", "tag4"]},
            {"title": "Entry 30", "content": "Content for entry 30", "tags": ["tag0", "tag0"]},
            {"title": "Entry 31", "content": "Content for entry 31", "tags": ["tag1", "tag1"]},
            {"title": "Entry 32", "content": "Content for entry 32", "tags": ["tag2", "tag2"]},
            {"title": "Entry 33", "content": "Content for entry 33", "tags": ["tag0", "tag3"]},
            {"title": "Entry 34", "content": "Content for entry 34", "tags": ["tag1", "tag4"]},
            {"title": "Entry 35", "content": "Content for entry 35", "tags": ["tag2", "tag0"]},
            {"title": "Entry 36", "content": "Content for entry 36", "tags": ["tag0", "tag1"]},
            {"title": "Entry 37", "content": "Content for entry 37", "tags": ["tag1", "tag2"]},
            {"title": "Entry 38", "content": "Content for entry 38", "tags": ["tag2", "tag3"]},
            {"title": "Entry 39", "content": "Content for entry 39", "tags": ["tag0", "tag4"]},
            {"title": "Entry 40", "content": "Content for entry 40", "tags": ["tag1", "tag0"]},
        ]

        for payload in sample_entries:
            status, _ = _request("POST", f"{self.base_url}/entry", payload)
            self.assertEqual(status, 201)

        status, entries = _request("GET", f"{self.base_url}/entries?query=Entry")
        self.assertEqual(status, 200)
        self.assertEqual(entries["data"]["total"], len(sample_entries))

    def test_pagination(self):
        for i in range(25):
            payload = {"title": f"Paginate {i}", "content": f"Content {i}"}
            status, _ = _request("POST", f"{self.base_url}/entry", payload)
            self.assertEqual(status, 201)

        status, data = _request("GET", f"{self.base_url}/entries?limit=10&offset=5")
        self.assertEqual(status, 200)
        self.assertEqual(data["data"]["limit"], 10)
        self.assertEqual(data["data"]["offset"], 5)
        self.assertEqual(len(data["data"]["items"]), 10)


if __name__ == "__main__":
    unittest.main()
