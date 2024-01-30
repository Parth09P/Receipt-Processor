from pydantic import BaseModel, constr, validator
from typing import List
import re

# Models based on the api.yml
class Item(BaseModel):
    shortDescription: constr(pattern=r"^[a-zA-Z0-9\s\-]+$")
    price: constr(pattern=r"^\d+\.\d{2}")
    
class ReceiptRequest(BaseModel):
    retailer: constr(strip_whitespace=True, pattern=r"^\S+$")
    purchaseDate: constr(strip_whitespace=True, pattern=r"^\d{4}-\d{2}-\d{2}$")
    purchaseTime: constr(strip_whitespace=True, pattern=r"^\d{2}:\d{2}$")
    items: List[Item]
    total: constr(strip_whitespace=True, pattern=r"^\d+\.\d{2}$")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {   
                    "retailer": "Target",
                    "purchaseDate": "2022-01-01",
                    "purchaseTime": "13:01",
                    "items": [
                        {"shortDescription": "Mountain Dew 12PK", "price": "6.49"},
                        {"shortDescription": "Emils Cheese Pizza", "price": "12.25"},
                        {"shortDescription": "Knorr Creamy Chicken", "price": "1.26"},
                        {"shortDescription": "Doritos Nacho Cheese", "price": "3.35"},
                        {"shortDescription": "Klarbrunn 12-PK 12 FL OZ", "price": "12.00"}
                    ],
                    "total": "35.35",
                }
            ]
        }
    }

# Validators to check for invalid inputs
@validator("retailer")
def validate_retailer(cls, value):
    if not re.match(r"^\S+$", value):
        raise ValueError("Retailer name must not contain whitespace characters.")
    return value

from datetime import datetime
@validator("purchaseDate")
def validate_purchase_date(cls, value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD.")
    
    return value

@validator("purchaseTime")
def validate_purchase_time(cls, value):
    try:
        datetime.strptime(value, "%H:%M")
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM.")
    
    return value

@validator("total")
def validate_total(cls, value):
    try:
        float(value)
    except ValueError:
        raise ValueError("Invalid total format. Use a decimal number with two digits after the dot.")
    
    return value
