"""
Sample payment processing module for CodeSense demo.

Contains typical e-commerce payment functions that the semantic search
engine should be able to discover using queries like:
  - "payment processing"
  - "credit card validation"
  - "tax calculation"
  - "invoice generation"
"""

import re
import time
import uuid


# ── Tax rates by region (demo data) ──────────────────────────────
TAX_RATES = {
    "US": 0.08,
    "EU": 0.20,
    "UK": 0.20,
    "IN": 0.18,
    "DEFAULT": 0.10,
}


def process_payment(amount, card_number, currency="USD"):
    """
    Process a payment transaction.

    Validates the card, calculates tax, and returns a transaction
    receipt.  In a real system this would integrate with a payment
    gateway like Stripe or Razorpay.
    """
    if not validate_card(card_number):
        return {"success": False, "error": "Invalid card number"}

    if amount <= 0:
        return {"success": False, "error": "Amount must be positive"}

    transaction_id = str(uuid.uuid4())
    timestamp = time.time()

    return {
        "success": True,
        "transaction_id": transaction_id,
        "amount": amount,
        "currency": currency,
        "timestamp": timestamp,
    }


def validate_card(card_number):
    """
    Validate a credit card number using the Luhn algorithm.

    Accepts the card number as a string (spaces and dashes are
    stripped automatically).
    """
    # Strip spaces and dashes
    card_number = re.sub(r"[\s-]", "", str(card_number))

    if not card_number.isdigit() or len(card_number) < 13:
        return False

    # Luhn algorithm
    total = 0
    reverse = card_number[::-1]
    for i, digit in enumerate(reverse):
        n = int(digit)
        if i % 2 == 1:
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return total % 10 == 0


def calculate_tax(amount, region="DEFAULT"):
    """
    Calculate tax for a given amount based on the customer's region.

    Returns a dict with the tax rate applied, tax amount, and total.
    """
    rate = TAX_RATES.get(region, TAX_RATES["DEFAULT"])
    tax_amount = round(amount * rate, 2)
    total = round(amount + tax_amount, 2)

    return {
        "subtotal": amount,
        "tax_rate": rate,
        "tax_amount": tax_amount,
        "total": total,
    }


def generate_invoice(transaction_id, items, customer_name, region="DEFAULT"):
    """
    Generate a simple invoice dict for a completed transaction.

    Parameters
    ----------
    transaction_id : str
        Unique transaction identifier.
    items : list[dict]
        Each item should have 'name', 'quantity', and 'price' keys.
    customer_name : str
        Name of the customer.
    region : str
        Region code for tax calculation.

    Returns
    -------
    dict
        Complete invoice with line items, tax breakdown, and totals.
    """
    subtotal = sum(item["price"] * item["quantity"] for item in items)
    tax_info = calculate_tax(subtotal, region)

    return {
        "invoice_id": f"INV-{transaction_id[:8].upper()}",
        "customer": customer_name,
        "items": items,
        "subtotal": tax_info["subtotal"],
        "tax_rate": tax_info["tax_rate"],
        "tax_amount": tax_info["tax_amount"],
        "total": tax_info["total"],
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }


def refund_payment(transaction_id, amount):
    """
    Process a refund for a previous transaction.

    In a real system this would reverse the charge through the
    payment gateway.
    """
    if amount <= 0:
        return {"success": False, "error": "Refund amount must be positive"}

    return {
        "success": True,
        "refund_id": str(uuid.uuid4()),
        "original_transaction": transaction_id,
        "refunded_amount": amount,
        "timestamp": time.time(),
    }
