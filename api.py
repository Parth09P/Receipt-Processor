from pydantic import ValidationError
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models import ReceiptRequest
from logic import calculate_points, generate_receipt_id

app = FastAPI()
response = {}  # A global dictionary to store the <uuid: points> pairs

@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    '''This function validates the input and would return 400 response in case of invalid receipts'''

    return JSONResponse(
        status_code=400,
        content={"description": "The receipt is invalid"},
    )

@app.post("/receipts/process", response_model=dict)
def process_receipt(receipt: ReceiptRequest):
    '''This API processes the receipt content and assigns a unique identifier to that receipt. In case the API is hit multiple times with the same data, the UUID would remain the same and would not be computed at every hit. This decision is made to avoid redundancy and storage optimization.'''

    try:
        points = calculate_points(receipt)
        receipt_id = generate_receipt_id(receipt)
        response[receipt_id] = points
        print(response)
        return {"id": receipt_id}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail="The receipt is invalid")

@app.get("/receipts/{id}/points", response_model=dict)
def get_points(id: str):
    '''This API retrieves the total number of points for the given receipt id.'''

    # Check if the ID exists in the response object
    if id not in response:
        raise HTTPException(status_code=404, detail="No receipt found for that ID")

    # Retrieve the points for the given receipt ID
    points = response[id]
    return {"points": points}

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def read_root():
    '''Default path'''

    with open("index.html", "r") as f:
        return HTMLResponse(content=f.read(), status_code=200)

