"""Country profiles for cash-on-delivery stores around the world.

COD is not a Pakistan-only story. It is how millions of small merchants
in South Asia, Africa, and the Middle East sell online, where cards are
rare and trust is built at the doorstep.

Each profile is deliberately small: currency, a mobile pattern, and a
landmark hint for the courier. Add a new country by adding one entry —
no code changes elsewhere.
"""

import re

COUNTRIES = {
    "PK": {
        "name": "Pakistan",
        "currency": "PKR",
        "currency_symbol": "Rs.",
        "phone_pattern": r"^03\d{2}-?\d{7}$",
        "phone_example": "0301-2345678",
        "landmark_hint": "near/opposite/chowk/bazaar/road",
    },
    "IN": {
        "name": "India",
        "currency": "INR",
        "currency_symbol": "₹",
        "phone_pattern": r"^(\+91[\s-]?)?[6-9]\d{9}$",
        "phone_example": "9876543210",
        "landmark_hint": "near/opposite/behind, street, area, landmark",
    },
    "BD": {
        "name": "Bangladesh",
        "currency": "BDT",
        "currency_symbol": "৳",
        "phone_pattern": r"^(\+880[\s-]?)?01[3-9]\d{8}$",
        "phone_example": "01712345678",
        "landmark_hint": "near/opposite, road, area, thana",
    },
    "NG": {
        "name": "Nigeria",
        "currency": "NGN",
        "currency_symbol": "₦",
        "phone_pattern": r"^(\+234[\s-]?)?0[789]\d{9}$",
        "phone_example": "08031234567",
        "landmark_hint": "near/opposite, street, estate, bus stop",
    },
    "EG": {
        "name": "Egypt",
        "currency": "EGP",
        "currency_symbol": "E£",
        "phone_pattern": r"^(\+20[\s-]?)?01\d{9}$",
        "phone_example": "01012345678",
        "landmark_hint": "near/opposite, street, district, building",
    },
    "AE": {
        "name": "United Arab Emirates",
        "currency": "AED",
        "currency_symbol": "AED ",
        "phone_pattern": r"^(\+971[\s-]?)?0?5\d{8}$",
        "phone_example": "0501234567",
        "landmark_hint": "near/opposite, building, area, street",
    },
}


def get_country(code):
    """Return a country profile, defaulting to Pakistan."""
    return COUNTRIES[code.upper()]


def valid_phone(phone, country_code="PK"):
    profile = get_country(country_code)
    cleaned = (phone or "").replace(" ", "")
    return bool(re.match(profile["phone_pattern"], cleaned))


def format_money(amount, country_code="PK"):
    profile = get_country(country_code)
    return f"{profile['currency_symbol']}{amount:,.0f}"
