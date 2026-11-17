def process_payment(amount):
    """Mock payment gateway. No real money or card details are used."""
    if amount <= 0:
        return "DECLINED"
    return "APPROVED"
