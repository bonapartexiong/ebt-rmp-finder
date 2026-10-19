"""Optional local server for the EBT RMP Finder.

Serves the frontend and proxies the two public data APIs through
/api/proxy, in case the browser blocks direct cross-origin calls.
Plain stdlib + Flask; no API keys needed.

Run:  python backend/proxy.py
Then open: http://localhost:5000/
"""
import json
import urllib.request
import urllib.error
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parent.parent
FRONTEND = ROOT / "frontend"
ALLOWED_HOSTS = {"api.zippopotam.us", "services1.arcgis.com"}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="text/html; charset=utf-8"):
        data = body.encode("utf-8") if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/health":
            return self._send(200, json.dumps({"ok": True}), "application/json")
        if parsed.path == "/api/proxy":
            target = parse_qs(parsed.query).get("u", [None])[0]
            if not target:
                return self._send(400, json.dumps({"error": "missing u param"}), "application/json")
            host = urlparse(target).netloc
            if host not in ALLOWED_HOSTS or not target.startswith("https://"):
                return self._send(403, json.dumps({"error": "host not allowed"}), "application/json")
            try:
                req = urllib.request.Request(target, headers={"User-Agent": "ebt-rmp-finder/1.0"})
                with urllib.request.urlopen(req, timeout=25) as resp:
                    body = resp.read()
                return self._send(200, body, "application/json")
            except urllib.error.URLError as e:
                return self._send(502, json.dumps({"error": str(e)}), "application/json")

        # Static files
        rel = parsed.path.lstrip("/") or "index.html"
        if ".." in rel:
            return self._send(403, "forbidden")
        f = FRONTEND / rel
        data_dir = ROOT / "data"
        if not f.exists() and (data_dir / rel).exists():
            f = data_dir / rel
        if not f.is_file():
            return self._send(404, "not found")
        ctype = "text/html; charset=utf-8"
        if f.suffix == ".json":
            ctype = "application/json"
        elif f.suffix == ".css":
            ctype = "text/css"
        elif f.suffix == ".js":
            ctype = "text/javascript"
        return self._send(200, f.read_bytes(), ctype)

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    srv = HTTPServer(("127.0.0.1", 5000), Handler)
    print("EBT RMP Finder: http://localhost:5000/")
    srv.serve_forever()
