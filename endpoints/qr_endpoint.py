import base64
import bz2
from io import BytesIO
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import os
import traceback
from fastapi import APIRouter, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
import qrcode
import base64
from qrcode.exceptions import DataOverflowError
from repos.qrrepos import read_docx_file, read_image_file, read_image_pdf, read_pdf_file, read_txt_file
from repos.validation import validate_input
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)


qrapp = APIRouter()

@qrapp.post("/generate_qrcode", tags=["QR Code"])
async def generate_qrcode(data: str):
    try:
        # Validate input data
        if not data.strip():
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Input data is a blank string.")
        
        constant="http://0.0.0.0:8080/decode_qrcode?encoded_data="

        # Compress the input data
        compressed_data = bz2.compress(data.encode('utf-8'), compresslevel=9)
        encoded_data = base64.urlsafe_b64encode(compressed_data).decode('utf-8')

        # Check the length of the encoded data
        max_length = 2550
        if len(encoded_data) > max_length:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"The length of the encoded string exceeds the limit of {max_length}. Current length: {len(encoded_data)}, which is {len(encoded_data) - max_length} characters more than the limit."
            )
        
        finalqr= constant+encoded_data

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(finalqr)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")


        return JSONResponse(status_code=HTTP_200_OK, content=img_str)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@qrapp.get("/decode_qrcode", tags=["QR Code"])
async def decode_qrcode(encoded_data: str):
    try:
        # Validate input data
        if not encoded_data:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Encoded data is required.")

        # Decode the base64 data
        try:
            compressed_data = base64.urlsafe_b64decode(encoded_data)
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Failed to decode base64 data: {str(e)}")

        # Decompress the data
        try:
            original_data = bz2.decompress(compressed_data).decode('utf-8')
        except Exception as e:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Failed to decompress data: {str(e)}")

        return JSONResponse(status_code=HTTP_200_OK, content=original_data)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")



@qrapp.post("/upload/" , tags=["QR Code"])
async def upload_file(file_type: str = Form(...), file: UploadFile = File(...)):
    extension = os.path.splitext(file.filename)[1].lower()

    # Validate file type based on selection
    if file_type == 'txt' or file_type == 'docx' or file_type == 'doc' or file_type=='json':
        if extension not in ['.txt', '.docx', '.doc', '.json']:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a .txt or .docx file.")
        if extension == '.txt':
            content = read_txt_file(file.file)
        elif extension == '.json':
            content = read_txt_file(file.file)
        else:
            content = read_docx_file(file.file)

    elif file_type == 'pdf':
        if extension != '.pdf':
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")
        
        try:
            
            content = read_pdf_file(file.file)
            if not content.strip():  
                content = read_image_pdf(file.file)  
        except Exception:
            content = read_image_pdf(file.file)

    elif file_type == 'image':
        if extension not in ['.jpeg', '.jpg', '.png']:
            raise HTTPException(status_code=400, detail="Invalid file type. Please upload a valid image (JPEG/PNG).")
        content = read_image_file(file.file)

    else:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    
    data = content
    print(data)
    try:
        if not data.strip():
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Input data is a blank string.")
        
        constant="http://0.0.0.0:8080/decode_qrcode?encoded_data="

        # Compress the input data
        compressed_data = bz2.compress(data.encode('utf-8'), compresslevel=9)
        encoded_data = base64.urlsafe_b64encode(compressed_data).decode('utf-8')
        print(len(encoded_data))
        max_length = 2650
        if len(encoded_data) > max_length:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail=f"The length of the encoded string exceeds the limit of {max_length}. Current length: {len(encoded_data)}, which is {len(encoded_data) - max_length} characters more than the limit."
            )
        
        finalqr= constant+encoded_data

        # Generate the QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(finalqr)
        qr.make(fit=True)

        # Create QR code image
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer)
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")


        return JSONResponse(status_code=HTTP_200_OK, content=img_str)
    

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An unexpected error occurred: {str(e)}")


@qrapp.get("/file-types/" , tags=["QR Code"])
def get_file_types():
    return {
        "file_types": ["txt", "docx", "doc" "pdf", "image"]
    }