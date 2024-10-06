from pydantic import BaseModel, Field, EmailStr
import traceback
from typing import Optional
from fastapi import APIRouter, UploadFile
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
import qrcode
import io
import base64
from fastapi.responses import JSONResponse
from fastapi import HTTPException

from model.Email import EmailQRRequest

emailapp = APIRouter()


@emailapp.post("/generate-email-qr/", tags=["Email"])
async def generate_email_qr(email_data: EmailQRRequest):
    try:
        email_qr_content = f"mailto:{email_data.email}"
        if email_data.subject:
            email_qr_content += f"?subject={email_data.subject}"
        if email_data.message:
            if "?" in email_qr_content:
                email_qr_content += f"&body={email_data.message}"
            else:
                email_qr_content += f"?body={email_data.message}"


        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(email_qr_content)
        qr.make(fit=True)

      
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

        if email_data.watermark_text:
            draw = ImageDraw.Draw(qr_img)
            font = ImageFont.load_default()

     
            text_bbox = draw.textbbox((0, 0), email_data.watermark_text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
            text_position = ((qr_img.size[0] - text_size[0]) // 2, (qr_img.size[1] - text_size[1]) // 2)


            draw.text(text_position, email_data.watermark_text, font=font, fill=(128, 128, 128, 128))


        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return JSONResponse(status_code=200, content=img_str)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
