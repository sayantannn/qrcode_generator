import base64
import traceback
from fastapi import APIRouter, FastAPI, HTTPException
from loguru import logger
from pydantic import BaseModel, EmailStr
import qrcode
import io
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.status import (
    HTTP_404_NOT_FOUND,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)

from model.VCard import VCardData

vcardapp = APIRouter()


from fastapi import UploadFile
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io
import base64
from fastapi.responses import JSONResponse
from fastapi import HTTPException

@vcardapp.post("/generate-vcard-qr/", tags=["Visiting Card"])
async def generate_vcard_qr(vcard_data: VCardData, watermark_text: str = None):
    try:
        # Updated vCard template with N (Name) and FN (Full Name) fields
        vcard_template = (
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            "N:{last_name};{first_name};;;\n"  # Last name first, then first name
            "FN:{fullname}\n"  # Full name
            "TEL;TYPE=CELL:{mobile}\n"
            "TEL;TYPE=HOME,VOICE:{phone}\n"
            "TEL;TYPE=FAX:{fax}\n"
            "EMAIL:{email}\n"
            "ORG:{company};{job}\n"
            "ADR;TYPE=HOME:;;{street};{city};{state};{zip};{country}\n"
            "URL:{website}\n"
            "END:VCARD"
        )

        # Generate vCard content, ensuring both N and FN are filled properly
        vcard_content = vcard_template.format(
            first_name=vcard_data.Firstname,
            last_name=vcard_data.Lastname,
            fullname=f"{vcard_data.Firstname} {vcard_data.Lastname}",  # Combine first and last name for FN field
            mobile=vcard_data.mobile,
            phone=vcard_data.phone or "",  # Fallback to empty string if None
            fax=vcard_data.fax or "",  # Fallback to empty string if None
            email=vcard_data.email,
            company=vcard_data.company or "",  # Fallback to empty string if None
            job=vcard_data.job or "",  # Fallback to empty string if None
            street=vcard_data.street or "",  # Fallback to empty string if None
            city=vcard_data.city or "",  # Fallback to empty string if None
            zip=vcard_data.zip or "",  # Fallback to empty string if None
            state=vcard_data.state or "",  # Fallback to empty string if None
            country=vcard_data.country or "",  # Fallback to empty string if None
            website=vcard_data.website or ""  # Fallback to empty string if None
        )

        # Generate QR code
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(vcard_content)
        qr.make(fit=True)

        # Convert to image
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        # Add watermark if provided
        if watermark_text:
            draw = ImageDraw.Draw(qr_img)
            font = ImageFont.load_default()  # Use default font
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

            # Position watermark in the center of the QR code
            text_position = (
                (qr_img.size[0] - text_size[0]) // 2,  # Center horizontally
                (qr_img.size[1] - text_size[1]) // 2   # Center vertically
            )

            watermark_color = (128, 128, 128, 128)  # Semi-transparent gray color
            draw.text(text_position, watermark_text, font=font, fill=watermark_color)

        # Save image to buffer
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Return base64-encoded image
        return JSONResponse(status_code=200, content=img_str)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")