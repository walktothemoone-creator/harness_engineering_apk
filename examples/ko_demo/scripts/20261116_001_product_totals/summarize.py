#!/usr/bin/env python3
"""Sum sales per product from a CSV with the header date,product,amount and print a Markdown table.

Usage:  python3 summarize.py <file.csv>
Reads only; the input file is never changed. Rows with an empty or non-numeric amount are skipped and counted.
"""
import csv
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation


def summarize(path):
    totals, skipped = defaultdict(Decimal), 0
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None or not {"date", "product", "amount"} <= set(reader.fieldnames):
            raise SystemExit("header must contain date,product,amount")
        for row in reader:
            try:
                amount = Decimal(row["amount"])
            except (InvalidOperation, TypeError):
                skipped += 1
                continue
            totals[row["product"].strip()] += amount
    return dict(totals), skipped


def to_markdown(totals, skipped):
    lines = ["| product | total |", "|---|---:|"]
    for name, amount in sorted(totals.items(), key=lambda kv: (-kv[1], kv[0])):
        lines.append(f"| {name} | {amount} |")
    lines.append(f"| **all** | **{sum(totals.values(), Decimal(0))}** |")
    if skipped:
        lines.append(f"\nskipped rows (empty or non-numeric amount): {skipped}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    print(to_markdown(*summarize(sys.argv[1])))
