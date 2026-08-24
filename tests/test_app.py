from __future__ import annotations

import pytest

from app import QuoteError, calculate_quote


def test_canadian_quote_uses_cad_and_complimentary_shipping() -> None:
    quote = calculate_quote(12_800, "CA")

    assert quote.currency == "CAD"
    assert quote.shipping_cents == 0
    assert quote.total_cents == 12_800


def test_us_quote_adds_shipping() -> None:
    quote = calculate_quote(12_800, "US")

    assert quote.currency == "USD"
    assert quote.shipping_cents == 1_200
    assert quote.total_cents == 14_000


@pytest.mark.parametrize("subtotal", (0, -1, 1_000_001, True, 12.8))
def test_rejects_invalid_subtotals(subtotal: object) -> None:
    with pytest.raises(QuoteError, match="subtotal_cents"):
        calculate_quote(subtotal, "US")  # type: ignore[arg-type]


def test_rejects_unsupported_country() -> None:
    with pytest.raises(QuoteError, match="country must be"):
        calculate_quote(12_800, "AU")
