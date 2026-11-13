"""Partial test suite (intentionally incomplete: gaps are what the agent will fill)."""
import pytest

from src.pricing.engine import (
    apply_tier_discount,
    calculate_subtotal,
    bulk_discount,
)


def test_subtotal_sums_price_times_quantity():
    items = [{"price": 10.0, "quantity": 2}, {"price": 5.5, "quantity": 1}]
    assert calculate_subtotal(items) == 25.5


def test_subtotal_rejects_negative_price():
    with pytest.raises(ValueError):
        calculate_subtotal([{"price": -1.0, "quantity": 1}])


@pytest.mark.parametrize("tier,expected", [("standard", 100.0), ("gold", 90.0)])
def test_tier_discount(tier, expected):
    assert apply_tier_discount(100.0, tier) == expected


def test_unknown_tier_raises():
    with pytest.raises(ValueError):
        apply_tier_discount(100.0, "diamond")

def test_bulk_discount():
    assert bulk_discount(1) == 0.0
