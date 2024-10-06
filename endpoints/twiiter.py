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

tweetapp = APIRouter()

@tweetapp.post("/generate-twitter-qr/", tags=["Twitter"])
async def generate_twitter_qr(
    option: str, 
    username: str = None, 
    tweet: Optional[str] = None, 
    watermark_text: str = None
):
    try:
   
        if option == "profile" and username:
            twitter_url = f"https://x.com/{username}"
        elif option == "tweet" and tweet:
            twitter_url = f"https://x.com/intent/tweet?text={tweet}"
            if len(tweet)>280:
                raise HTTPException(status_code=400, detail="Lenght of tweet exceeded the permisible limit")
        else:
            raise HTTPException(status_code=400, detail="Invalid option or missing required data.")
        
        
      
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
        qr.add_data(twitter_url)
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
