from __future__ import annotations

import os
import sys

import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config  # noqa: E402

BASE = config.API_BASE_URL
NEW = {"reading_ts": "2030-01-01T00:00:00", "appliances_wh": 123, "lights_wh": 5}
UPD = {"appliances_wh": 999, "lights_wh": 9}
passed = 0
failed = 0


def check(label: str, cond: bool) -> None:
    global passed, failed
    ok = bool(cond)
    passed += int(ok)
    failed += int(not ok)
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}")


def test_db(prefix: str) -> None:
    print(f"\n=== {prefix} ===")
    try:
        latest = requests.get(f"{BASE}{prefix}/latest", timeout=10)
        check("GET /latest -> 200", latest.status_code == 200)

        ranged = requests.get(
            f"{BASE}{prefix}/range",
            params={"start": "2016-01-11T17:00:00", "end": "2016-01-11T18:00:00"},
            timeout=10,
        )
        check("GET /range -> 200 & list", ranged.status_code == 200 and isinstance(ranged.json(), list))
        check("GET /range -> non-empty for seeded window", len(ranged.json()) > 0)

        created = requests.post(f"{BASE}{prefix}", json=NEW, timeout=10)
        check("POST -> 201", created.status_code == 201)
        reading_id = created.json()["reading_id"]

        fetched = requests.get(f"{BASE}{prefix}/{reading_id}", timeout=10)
        check(
            "GET /{id} -> 200 & correct value",
            fetched.status_code == 200 and fetched.json()["appliances_wh"] == 123,
        )

        updated = requests.put(f"{BASE}{prefix}/{reading_id}", json=UPD, timeout=10)
        check(
            "PUT /{id} -> updated value",
            updated.status_code == 200 and updated.json()["appliances_wh"] == 999,
        )

        deleted = requests.delete(f"{BASE}{prefix}/{reading_id}", timeout=10)
        check("DELETE /{id} -> 200", deleted.status_code == 200)

        missing = requests.get(f"{BASE}{prefix}/{reading_id}", timeout=10)
        check("GET deleted -> 404", missing.status_code == 404)
    except requests.RequestException as exc:
        check(f"connection ({exc})", False)


def test_mongo_window() -> None:
    print("\n=== /mongo/readings/window ===")
    try:
        response = requests.get(f"{BASE}/mongo/readings/window", params={"n": 50}, timeout=15)
        check("GET /window -> 200", response.status_code == 200)
        rows = response.json()
        check("GET /window -> list of 50", isinstance(rows, list) and len(rows) == 50)
        if rows:
            sample = rows[0]
            check("GET /window -> has Appliances", "Appliances" in sample)
            check("GET /window -> has date", "date" in sample)
    except requests.RequestException as exc:
        check(f"connection ({exc})", False)


if __name__ == "__main__":
    print(f"Testing API at {BASE}")
    health = requests.get(f"{BASE}/health", timeout=5)
    check("GET /health -> 200", health.status_code == 200 and health.json().get("status") == "ok")
    test_db("/sql/readings")
    test_db("/mongo/readings")
    test_mongo_window()
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
