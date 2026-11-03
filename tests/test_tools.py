import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from store_tools.countries import format_money, valid_phone
from store_tools.order_check import check_order, format_order_summary
from store_tools.parcels import classify_all
from store_tools.returns import analyse_returns


def good_order():
    return {
        "name": "Test Customer",
        "phone": "0301-2345678",
        "address": "Near Main Bazaar, Faisalabad",
        "zip": "",
        "note": "OK WA",
        "payment": "COD",
        "items": [{"product": "Marco Polo Suiting", "variant": "Black",
                  "qty": 1, "price": 4280}],
    }


def test_good_order_passes():
    assert check_order(good_order()) == []


def test_zip_and_missing_landmark_fail():
    order = good_order()
    order["zip"] = "38000"
    order["address"] = "Faisalabad"
    problems = check_order(order)
    assert any("ZIP" in p for p in problems)
    assert any("landmark" in p for p in problems)


def test_summary_total():
    summary = format_order_summary(good_order())
    assert "Rs.4,280" in summary


def test_returns_rate():
    rows = [
        {"order_id": "1", "courier": "Leopards", "total": "4280",
         "status": "delivered"},
        {"order_id": "2", "courier": "Leopards", "total": "4280",
         "status": "returned"},
        {"order_id": "3", "courier": "PostEx", "total": "3695",
         "status": "mystery"},
    ]
    result = analyse_returns(rows)
    assert result["return_rate_pct"] == 50.0
    assert result["unknown_status_order_ids"] == ["3"]


def test_international_phone_and_money():
    assert valid_phone("9876543210", "IN")
    assert not valid_phone("0301-2345678", "IN")
    assert format_money(1299, "IN") == "₹1,299"
    assert format_money(4280, "PK") == "Rs.4,280"


def test_india_order_passes_with_zip():
    order = {
        "name": "Test Customer India",
        "phone": "9876543210",
        "address": "Near MG Road, Pune",
        "zip": "411001",
        "note": "OK WA",
        "payment": "COD",
        "country": "IN",
        "items": [{"product": "Cotton Kurta", "variant": "Blue",
                  "qty": 1, "price": 1299}],
    }
    assert check_order(order) == []
    assert "₹1,299" in format_order_summary(order)


def test_parcel_buckets():
    rows = [
        {"consignment": "A", "status": "in_transit",
         "last_update_days_ago": 0},
        {"consignment": "B", "status": "in_transit",
         "last_update_days_ago": 5},
        {"consignment": "C", "status": "in_transit",
         "last_update_days_ago": None},
    ]
    buckets = classify_all(rows)
    assert buckets["normal"] == ["A"]
    assert buckets["stuck_48h_plus"] == ["B"]
    assert buckets["never_picked_up"] == ["C"]
