"""Client for the public AI HOT API."""

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://aihot.virxact.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


class AihotClientError(RuntimeError):
    """Raised when AI HOT cannot be fetched or parsed."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def iso_hours_ago(hours: int, now: datetime | None = None) -> str:
    current = now or utc_now()
    return (current - timedelta(hours=hours)).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def fetch_selected_items(hours: int = 24, take: int = 100) -> list[dict[str, Any]]:
    """Fetch selected AI HOT items for a rolling time window."""

    params = {
        "mode": "selected",
        "since": iso_hours_ago(hours),
        "take": str(take),
    }
    url = f"{BASE_URL}/api/public/items?{urlencode(params)}"
    payload = _fetch_json(url)
    items = payload.get("items")
    if not isinstance(items, list):
        raise AihotClientError("AI HOT response did not contain an items list.")
    return [item for item in items if isinstance(item, dict)]


def _fetch_json(url: str) -> dict[str, Any]:
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
    try:
        with urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise AihotClientError(f"AI HOT request failed with HTTP {exc.code}: {body}") from exc
    except URLError as exc:
        raise AihotClientError(f"AI HOT request failed: {exc.reason}") from exc
    except TimeoutError as exc:
        raise AihotClientError("AI HOT request timed out.") from exc

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise AihotClientError("AI HOT response was not valid JSON.") from exc

    if not isinstance(data, dict):
        raise AihotClientError("AI HOT response was not a JSON object.")
    return data

