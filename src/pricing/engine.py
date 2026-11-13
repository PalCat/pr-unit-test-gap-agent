"""Order pricing: subtotal, tier discount, coupons, shipping, total.

Business rules live in docs/rules.md (the source of truth for tests).
"""
from datetime import date

TIER_DISCOUNTS = {"standard": 0.00, "silver": 0.05, "gold": 0.10, "platinum": 0.15}

COUPONS = {
    "SAVE10": {"type": "percent", "value": 0.10, "min_subtotal": 50.0, "expires": date(2026, 12, 31)},
    "FLAT20": {"type": "flat", "value": 20.0, "min_subtotal": 100.0, "expires": None},
}

DOMESTIC_FREE_SHIPPING_THRESHOLD = 100.0
DOMESTIC_SHIPPING_FEE = 8.99
INTERNATIONAL_SHIPPING_FEE = 24.99


def calculate_subtotal(items):
    """Sum price * quantity. Each item is {"price": float, "quantity": int}."""
    total = 0.0
    for item in items:
        price, qty = item["price"], item["quantity"]
        if price < 0:
            raise ValueError("price must be >= 0")
        if not isinstance(qty, int) or qty < 1:
            raise ValueError("quantity must be an integer >= 1")
        total += price * qty
        #adding comment to create a PR without change required for unit tests
    return round(total, 2)


def apply_tier_discount(subtotal, tier):
    """Return subtotal after the customer-tier percentage discount."""
    if tier not in TIER_DISCOUNTS:
        raise ValueError(f"unknown tier: {tier}")
    return round(subtotal * (1 - TIER_DISCOUNTS[tier]), 2)


def validate_coupon(code, subtotal, today=None):
    """Return the coupon dict if usable for this subtotal and date, else raise ValueError."""
    today = today or date.today()
    coupon = COUPONS.get(code)
    if coupon is None:
        raise ValueError(f"invalid coupon: {code}")
    if coupon["expires"] is not None and today > coupon["expires"]:
        raise ValueError(f"coupon expired: {code}")
    if subtotal < coupon["min_subtotal"]:
        raise ValueError(f"minimum subtotal not met for {code}")
    return coupon


def apply_coupon(subtotal, code, today=None):
    """Return subtotal after the coupon; never below zero."""
    coupon = validate_coupon(code, subtotal, today)
    if coupon["type"] == "percent":
        discounted = subtotal * (1 - coupon["value"])
    else:
        discounted = subtotal - coupon["value"]
    return round(max(discounted, 0.0), 2)


def calculate_shipping(amount, country):
    """Domestic (US) ships free at/above the threshold; international is a flat fee."""
    if country == "US":
        return 0.0 if amount >= DOMESTIC_FREE_SHIPPING_THRESHOLD else DOMESTIC_SHIPPING_FEE
    return INTERNATIONAL_SHIPPING_FEE


def calculate_order_total(items, tier="standard", coupon=None, country="US", today=None):
    """Full order total: subtotal -> tier discount -> coupon -> shipping."""
    amount = calculate_subtotal(items)
    amount = apply_tier_discount(amount, tier)
    if coupon:
        amount = apply_coupon(amount, coupon, today)
    amount += calculate_shipping(amount, country)
    return round(amount, 2)

def bulk_discount(quantity):
    if quantity >= 10:
        return 0.1
    return 0.0
