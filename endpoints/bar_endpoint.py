import base64
from io import BytesIO
import logging
import traceback
from typing import Optional
import barcode
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from loguru import logger
from model.Barcode import BarcodeType
from repos.validation import validate_input
from barcode.writer import ImageWriter
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)



barapp = APIRouter()

logger = logging.getLogger("/barcode_logger")
logging.basicConfig(level=logging.DEBUG)

# Supported barcode types
SUPPORTED_BARCODE_TYPES = {
    "ean8": barcode.get_barcode_class("ean8"),
    "ean13": barcode.get_barcode_class("ean13"),
    "upca": barcode.get_barcode_class("upca"),
    "code39": barcode.get_barcode_class("code39"),
    "code128": barcode.get_barcode_class("code128"),
    "isbn13": barcode.get_barcode_class("isbn13"),
    "pzn": barcode.get_barcode_class("pzn"),
  
}

def validate_input(data: str, code_type: str):
    if code_type == "ean13" and len(data) != 12:
        raise ValueError("EAN13 barcode must have 12 digits (without the checksum).")
    if code_type == "ean8" and len(data) != 7:
        raise ValueError("EAN8 barcode must have 7 digits (without the checksum).")
    if code_type == "upca" and len(data) != 11:
        raise ValueError("UPCA barcode must have 11 digits (without the checksum).")
    if code_type == "isbn13" and len(data) != 12:
        raise ValueError("ISBN13 barcode must have 12 digits (without the checksum).")
    if code_type == "pzn" and len(data) != 7:
        raise ValueError("PZN barcode must have 7 digits.")
    if code_type in ["code39", "code128"]:
        if not data.isalnum():
            raise ValueError(f"{code_type.upper()} barcode must consist of alphanumeric characters.")
    if code_type in ["ean13", "ean8", "upca", "isbn13", "pzn"] and not data.isdigit():
        raise ValueError(f"The barcode data for {code_type.upper()} must be numeric.")


@barapp.post("/generate_barcode", tags=["Barcode"])
async def generate_barcode(
    data: str = Query(..., description="The data to encode into the barcode."),
    code_type: str = Query("ean13", description="The type of barcode to generate. Supported types: ean8, ean13, upca, code39, code128, isbn13, pzn."),
    output_format: Optional[str] = Query("png", description="Output format: png or svg."),
):
    try:
    
        if code_type not in SUPPORTED_BARCODE_TYPES:
            raise HTTPException(status_code=400, detail=f"Unsupported barcode type: {code_type}")


        validate_input(data, code_type)

        BarcodeClass = SUPPORTED_BARCODE_TYPES[code_type]
        writer_options = {}

        if output_format == "png":
            writer = ImageWriter()
        elif output_format == "svg":
            writer = None 
        else:
            raise HTTPException(status_code=400, detail="Invalid output format. Use 'png' or 'svg'.")

        barcode_instance = BarcodeClass(data, writer=writer)

       
        buffer = BytesIO()
        barcode_instance.write(buffer, options=writer_options)
        buffer.seek(0)

        if output_format == "png":
            img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")
        else:
            img_str = buffer.getvalue().decode("utf-8")

       
        return JSONResponse(status_code=HTTP_200_OK, content=img_str)

    except ValueError as ve:
        logger.debug(traceback.format_exc())
        logger.error(f"Validation error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))

    except Exception as e:
        logger.debug(traceback.format_exc())
        logger.error(f"Unexpected error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")
    



SUPPORTED_BARCODE_TYPES = {
    "ean8": "EAN-8",
    "ean13": "EAN-13",
    "upca": "UPCA",
    "code39": "Code 39",
    "code128": "Code 128",
    "isbn13": "ISBN-13",
    "pzn": "PZN"
}


@barapp.get("/barcode/types", response_model=list[BarcodeType], tags=["Barcode"])
async def get_barcode_types():
    try:
        return [{"code": code, "name": name} for code, name in SUPPORTED_BARCODE_TYPES.items()]
    except Exception as e: 
        logger.debug(traceback.format_exc())
        logger.error(f"Unexpected error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {e}")