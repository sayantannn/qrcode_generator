import traceback
from fastapi import APIRouter, UploadFile
from PIL import Image, ImageDraw, ImageFont
from loguru import logger
import qrcode
import io
import base64
from fastapi.responses import JSONResponse
from fastapi import HTTPException

wifiapp = APIRouter()

@wifiapp.post("/generate-wifi-qr/", tags=["Wifi Scanner"])
async def generate_wifi_qr(ssid: str, password: str, encryption: str, hidden: bool = False, watermark_text: str = None):
    try:
        #type should be WPA, WEP, or nopass
        wifi_qr_content = f"WIFI:S:{ssid};T:{encryption};P:{password};H:{'true' if hidden else 'false'};;"

     
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(wifi_qr_content)
        qr.make(fit=True)

        
        qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")

       
        if watermark_text:
           
            draw = ImageDraw.Draw(qr_img)
            font = ImageFont.load_default() 
            text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])

         
            text_position = (
                (qr_img.size[0] - text_size[0]) // 2,  
                (qr_img.size[1] - text_size[1]) // 2  
            )

          
            watermark_color = (128, 128, 128, 128)  

            draw.text(text_position, watermark_text, font=font, fill=watermark_color)

        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return JSONResponse(status_code=200, content=img_str)

    except Exception as e:
        logger.debug(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
