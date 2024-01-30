import uuid
import math

from models import ReceiptRequest

def calculate_points(receipt: ReceiptRequest) -> int:
    '''This function calculates the total number of points for the receipt based on the rules provided in the design document.'''

    # Rule 1: One point for every alphanumeric character in the retailer name.
    points = len([char for char in receipt.retailer if char.isalnum()])

    # Rule 2: 50 points if the total is a round dollar amount with no cents.
    if receipt.total.endswith(".00"):
        points += 50

    # Rule 3: 25 points if the total is a multiple of 0.25.
    if float(receipt.total) % 0.25 == 0:
        points += 25

    # Rule 4: 5 points for every two items on the receipt.
    points += 5 * (len(receipt.items) // 2)

    # Rule 5: If the trimmed length of the item description is a multiple of 3,
    # multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in receipt.items:
        trimmed_length = len(item.shortDescription.strip())
        if trimmed_length % 3 == 0:
            item_points = math.ceil(float(item.price) * 0.2)
            points += item_points

    # Rule 6: 6 points if the day in the purchase date is odd.
    purchase_day = int(receipt.purchaseDate.split("-")[2])
    if purchase_day % 2 != 0:
        points += 6

    # Rule 7: 10 points if the time of purchase is after 2:00 pm and before 4:00 pm.
    purchase_time = int(receipt.purchaseTime.split(":")[0])
    if 14 <= purchase_time < 16:
        points += 10

    return points


def generate_receipt_id(receipt) -> str:
    '''This function assigns a unique identifier to the receipt object. For storage optimization, the same ID would be assigned if the API is hit multiple times with same input data. If the data is changed, a new UUID would be generated'''
    input_str = str(receipt)
    receipt_id = str(uuid.uuid5(uuid.NAMESPACE_OID, input_str))
    
    return receipt_id
