import base64
from io import BytesIO
import traceback
from fastapi import FastAPI, HTTPException, Query, logger
import qrcode
from qrcode.exceptions import DataOverflowError

def validate_input(data: str, code_type: str) -> bool:
    """
    Validates the input for QR code and barcode generation.
    :param data: The input data to validate.
    :param code_type: The type of code (either "qr" or "barcode").
    :return: True if input is valid, raises HTTPException if not.
    """
    if not data:
        raise HTTPException(status_code=400, detail="Input cannot be empty.")
    
    if code_type == "qr":
        if len(data) > 4296:
            raise HTTPException(status_code=400, detail="Input is too long for a QR code.")
    elif code_type == "barcode":
        # Barcode has stricter length constraints (e.g., EAN-13 uses 12 digits)
        if not data.isdigit() or len(data) > 128:
            raise HTTPException(status_code=400, detail="Barcodes require numeric input of up to 12 digits.")
    else:
        raise HTTPException(status_code=400, detail="Invalid code type.")
    
    return True
