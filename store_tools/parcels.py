"""Classify parcels from a simple timeline export.

Input rows: consignment, courier, last_update_days_ago, status
where status is: in_transit, out_for_delivery, delivered, returned,
or return_in_transit.

Buckets (matching the daily store check):
- normal: in transit, updated within 48 hours
- stuck_48h_plus: in transit, no update for 48 hours or more
- never_picked_up: in transit with no update at all (days = None)
- delivered / returned / return_pipeline: as reported by the courier
"""

STUCK_AFTER_DAYS = 2


def classify_parcel(row):
    status = (row.get("status") or "").strip().lower()
    days = row.get("last_update_days_ago")
    if status == "delivered":
        return "delivered"
    if status == "returned":
        return "returned"
    if status == "return_in_transit":
        return "return_pipeline"
    if status in ("in_transit", "out_for_delivery"):
        if days is None:
            return "never_picked_up"
        if days >= STUCK_AFTER_DAYS:
            return "stuck_48h_plus"
        return "normal"
    return "data_problem"


def classify_all(rows):
    buckets = {}
    for row in rows:
        buckets.setdefault(classify_parcel(row), []).append(
            row.get("consignment"))
    return buckets
