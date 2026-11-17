"""Evaluate three CSV deduplication strategies on a small synthetic benchmark."""

import csv
import io
import json
from pathlib import Path


def read_csv(text):
    """Parse CSV into immutable rows while preserving string values."""
    return tuple(map(tuple, csv.reader(io.StringIO(text, newline=""), strict=True)))


def exact_rows(rows):
    return tuple(dict.fromkeys(rows))


def first_row_per_id(rows):
    selected = {}
    for row in rows:
        selected.setdefault(row[0], row)
    return tuple(selected.values())


def nonempty_rows(rows):
    return exact_rows(row for row in rows if all(row))


CANDIDATES = {
    "exact-rows": exact_rows,
    "first-row-per-id": first_row_per_id,
    "nonempty-rows": nonempty_rows,
}


def load_fixtures():
    path = Path(__file__).with_name("fixtures.json")
    return json.loads(path.read_text(encoding="utf-8"))


def run_evaluation(fixtures):
    for candidate_id, candidate in CANDIDATES.items():
        for fixture in fixtures:
            header, *rows = read_csv(fixture["input"])
            expected = read_csv(fixture["expected"])
            actual = (header, *candidate(rows))
            yield {
                "candidate": candidate_id,
                "fixture": fixture["id"],
                "passed": actual == expected,
                "expected": expected,
                "actual": actual,
            }


def main():
    fixtures = load_fixtures()
    passed = dict.fromkeys(CANDIDATES, 0)
    for result in run_evaluation(fixtures):
        candidate = result["candidate"]
        if result["passed"]:
            passed[candidate] += 1
            continue
        print(f"FAIL: {candidate} / {result['fixture']}")
        print(f"  Expected rows: {result['expected'][1:]}")
        print(f"  Actual rows:   {result['actual'][1:]}")

    print("\nResults")
    for candidate, count in passed.items():
        print(f"  {candidate}: {count}/{len(fixtures)} passed")


if __name__ == "__main__":
    main()
