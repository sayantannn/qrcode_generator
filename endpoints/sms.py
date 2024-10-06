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

from model.SMS import SMSQRRequest

smsapp = APIRouter()



@smsapp.post("/generate-sms-qr/", tags=["SMS"])
async def generate_sms_qr(sms_data: SMSQRRequest):
    try:
       
        sms_qr_content = f"sms:{sms_data.phone_number}"
        if sms_data.message:
            sms_qr_content += f"?body={sms_data.message}"

      
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(sms_qr_content)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

    
        if sms_data.watermark_text:
            draw = ImageDraw.Draw(qr_img)
            font = ImageFont.load_default()

        
            text_bbox = draw.textbbox((0, 0), sms_data.watermark_text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
            text_position = ((qr_img.size[0] - text_size[0]) // 2, (qr_img.size[1] - text_size[1]) // 2)

           
            draw.text(text_position, sms_data.watermark_text, font=font, fill=(128, 128, 128, 128))

     
        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return JSONResponse(status_code=200, content=img_str)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
