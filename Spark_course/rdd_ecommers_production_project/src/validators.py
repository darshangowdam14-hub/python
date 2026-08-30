VALID_STATUSES={
    "SUCCESS",
    "FAILED",
    "PENDING"
}

def validate_transactions(fields):
    errors=[]
    transaction_id=fields[0]
    customer_id=fields[1]
    product_id=fields[2]
    product_name=fields[3]
    category=fields[4]

    quantity=fields[5]
    unit_price=fields[6]
    amount=fields[7]

    payment_method=fields[8]
    status=fields[9]
    transaction_timestamp=fields[10]
    city=fields[11]

    if not transaction_id:
        errors.append("MISSING TRANSACTION ID")
    if not customer_id:
        errors.append("MISSING CUSTOMER ID")
    if quantity<=0:
        errors.append("INVALID_QUANTITY")
    if unit_price<=0:
        errors.append("INVALID_UNIT_PRICE")
    if amount<=0:
        errors.append("INVALID AMOUNT")
    expected_amount=quantity*unit_price
    if amount!=expected_amount:
        errors.append("AMOUNT_MISMATCH")
    
    if not payment_method:
        errors.append("MISSING PAYMENT_METHOD")
    if status not in VALID_STATUSES:
        errors.append("INVALID STATUS")
    if not city:
        errors.append("MISSING_CITY")
    if errors:
        return(
            "INVALID",
            fields,
            errors
        )
    return(
        "VALID",
        fields,
        None
    )