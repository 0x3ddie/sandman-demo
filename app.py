from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

STATIC_ROOT = Path(__file__).parent / "static"
MAX_REQUEST_BYTES = 64 * 1024

COUNTRY_CONFIG = {
    "US": ("USD", 1200),
    "ca": ("CAD", 0),
    "GB": ("GBP", 1800),
}
SUPPORTED_COUNTRIES = frozenset({"US", "CA", "GB"})


class QuoteError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class Quote:
    currency: str
    subtotal_cents: int
    shipping_cents: int
    total_cents: int


def calculate_quote(subtotal_cents: int, country: str) -> Quote:
    if isinstance(subtotal_cents, bool) or not isinstance(subtotal_cents, int):
        raise QuoteError("subtotal_cents must be an integer")
    if not 0 < subtotal_cents <= 1_000_000:
        raise QuoteError("subtotal_cents must be between 1 and 1000000")
    normalized_country = country.strip().upper()
    if normalized_country not in SUPPORTED_COUNTRIES:
        raise QuoteError("country must be one of US, CA, or GB")
    currency, shipping_cents = COUNTRY_CONFIG[normalized_country]
    return Quote(
        currency=currency,
        subtotal_cents=subtotal_cents,
        shipping_cents=shipping_cents,
        total_cents=subtotal_cents + shipping_cents,
    )


class StorefrontHandler(BaseHTTPRequestHandler):
    server_version = "Northstar/1.0"

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(HTTPStatus.OK, {"status": "ok", "service": "northstar-store"})
            return
        static_file = {
            "/": "index.html",
            "/app.js": "app.js",
            "/styles.css": "styles.css",
        }.get(self.path)
        if static_file is None:
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        content_type = "text/html; charset=utf-8"
        if static_file.endswith(".js"):
            content_type = "text/javascript; charset=utf-8"
        elif static_file.endswith(".css"):
            content_type = "text/css; charset=utf-8"
        self._send_bytes(HTTPStatus.OK, (STATIC_ROOT / static_file).read_bytes(), content_type)

    def do_POST(self) -> None:
        if self.path != "/api/checkout/quote":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "not found"})
            return
        try:
            payload = self._read_json()
            quote = calculate_quote(payload.get("subtotal_cents"), str(payload.get("country", "")))
        except (json.JSONDecodeError, QuoteError) as error:
            self._send_json(HTTPStatus.BAD_REQUEST, {"error": str(error)})
            return
        except Exception:
            self._send_json(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": "We could not refresh your total. Please try again."},
            )
            return
        self._send_json(HTTPStatus.OK, asdict(quote))

    def _read_json(self) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as error:
            raise QuoteError("invalid Content-Length") from error
        if not 0 < length <= MAX_REQUEST_BYTES:
            raise QuoteError("request body must be between 1 and 65536 bytes")
        payload = json.loads(self.rfile.read(length))
        if not isinstance(payload, dict):
            raise QuoteError("request body must be a JSON object")
        return payload

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, separators=(",", ":")).encode()
        self._send_bytes(status, body, "application/json; charset=utf-8")

    def _send_bytes(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)


def main() -> None:
    port = int(os.getenv("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), StorefrontHandler)
    print(f"Northstar listening on http://0.0.0.0:{port}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
