"""Check a COD order against the rules that prevent courier returns.

Rules encoded here come from a real Faisalabad COD store:
- guest checkout, COD only, cart note "OK WA"
- postal/ZIP field left EMPTY (courier slips in Pakistan do not use it)
- address short and aligned with the nearest famous landmark
- "Allow to Open" only when the customer explicitly asked for it
- Pakistani mobile in 03XX-XXXXXXX form

This is a checklist, not a Shopify API client. It never places an order.
"""

from .countries import format_money, get_country, valid_phone

LANDMARK_WORDS = ("near", "opposite", "behind", "adjacent", "chowk",
                   "bazaar", "market", "plaza", "road", "gali", "mohallah",
                   "street", "area", "estate", "bus stop", "building")


def check_order(order, country_code=None):
    """order: dict with name, phone, address, zip, note, payment, items.

    country_code defaults to order["country"] or "PK".
    Returns a list of problem strings; empty means the order passes.
    """
    country_code = country_code or order.get("country") or "PK"
    profile = get_country(country_code)
    problems = []
    if not order.get("name"):
        problems.append("Missing customer name.")
    if not valid_phone(order.get("phone"), country_code):
        problems.append(f"Phone '{order.get('phone')}' is not a valid "
                        f"{profile['name']} mobile "
                        f"(example: {profile['phone_example']}).")
    address = order.get("address") or ""
    if len(address) < 10:
        problems.append("Address is too short for a courier to find.")
    if len(address) > 200:
        problems.append("Address is too long; shorten it to the landmark.")
    lowered = address.lower()
    if not any(word in lowered for word in LANDMARK_WORDS):
        problems.append("Address has no landmark (near/opposite/chowk/"
                        "bazaar/road) for the courier.")
    if country_code == "PK" and order.get("zip"):
        problems.append("ZIP/postal field must be left EMPTY for "
                        "Pakistan courier slips in this flow.")
    if (order.get("payment") or "").upper() != "COD":
        problems.append("Payment must be COD for this checklist.")
    note = order.get("note") or ""
    if "OK WA" not in note:
        problems.append('Cart note must contain "OK WA".')
    if not order.get("items"):
        problems.append("No line items.")
    return problems


def format_order_summary(order, country_code=None):
    """One send-ready summary line per order, for final review."""
    country_code = country_code or order.get("country") or "PK"
    items = ", ".join(
        f"{i.get('product')} ({i.get('variant', '')}) x{i.get('qty', 1)}"
        for i in order.get("items", []))
    total = sum(i.get("price", 0) * i.get("qty", 1)
                for i in order.get("items", []))
    return (f"{order.get('name')} | {order.get('phone')} | {items} | "
            f"{format_money(total, country_code)} | "
            f"{order.get('address')}")
