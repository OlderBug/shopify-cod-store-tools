"""Return-rate math for a Shopify orders CSV export.

Expected columns (at least): order_id, courier, total, status
where status is one of: delivered, returned, in_transit, cancelled.

No totals are guessed: rows with an unknown status are reported
separately and never counted as delivered or returned.
"""

import csv
from collections import Counter, defaultdict


def analyse_returns(rows):
    totals = Counter()
    amounts = defaultdict(float)
    unknown = []
    for row in rows:
        status = (row.get("status") or "").strip().lower()
        if status not in ("delivered", "returned", "in_transit", "cancelled"):
            unknown.append(row.get("order_id"))
            continue
        totals[status] += 1
        try:
            amounts[status] += float(row.get("total") or 0)
        except ValueError:
            pass
    delivered = totals["delivered"]
    returned = totals["returned"]
    closed = delivered + returned
    rate = (returned / closed * 100) if closed else 0.0
    return {
        "delivered_count": delivered,
        "returned_count": returned,
        "in_transit_count": totals["in_transit"],
        "cancelled_count": totals["cancelled"],
        "return_rate_pct": round(rate, 1),
        "returned_amount": round(amounts["returned"], 2),
        "unknown_status_order_ids": unknown,
    }


def analyse_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return analyse_returns(list(csv.DictReader(handle)))
