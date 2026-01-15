import json
import os
import tempfile
import threading
import time
import unittest
import urllib.request
import urllib.error

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


class APITestCase(unittest.TestCase):
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

    def test_health_endpoint(self):
        status, payload = _request("GET", f"{self.base_url}/health")
        self.assertEqual(status, 200)
        self.assertEqual(payload["status"], "success")
        self.assertEqual(payload["data"]["status"], "ok")

    def test_entry_crud_flow(self):
        payload = {
            "title": "Test Entry",
            "content": "This is a test entry content",
            "tags": ["test", "api"],
        }
        status, created = _request("POST", f"{self.base_url}/entry", payload)
        self.assertEqual(status, 201)
        entry_id = created["data"]["id"]

        status, entries = _request("GET", f"{self.base_url}/entries?query=test")
        self.assertEqual(status, 200)
        self.assertEqual(entries["data"]["total"], 1)

        status, _ = _request("GET", f"{self.base_url}/entry/{entry_id}")
        self.assertEqual(status, 200)

        update_payload = {
            "title": "Updated Title",
            "content": "Updated content for entry",
            "tags": "updated,api",
        }
        status, updated = _request("PUT", f"{self.base_url}/entry/{entry_id}", update_payload)
        self.assertEqual(status, 200)
        self.assertEqual(updated["data"]["title"], "Updated Title")

        status, _ = _request("DELETE", f"{self.base_url}/entry/{entry_id}")
        self.assertEqual(status, 200)

        with self.assertRaises(urllib.error.HTTPError) as context:
            _request("GET", f"{self.base_url}/entry/{entry_id}")
        self.assertEqual(context.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
