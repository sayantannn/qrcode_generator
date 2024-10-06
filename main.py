from fastapi import FastAPI, HTTPException, Query
from qrcode.exceptions import DataOverflowError
from io import BytesIO
import base64
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import qrcode
import base64
from endpoints.qr_endpoint import qrapp
from endpoints.bar_endpoint import barapp
from endpoints.vcard import vcardapp
from endpoints.wifi import wifiapp
from endpoints.twiiter import tweetapp
from endpoints.email import emailapp
from endpoints.sms import smsapp
from io import BytesIO



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # You can restrict this to specific methods if needed
    allow_headers=["*"],  # You can restrict this to specific headers if needed
)

app.include_router(qrapp)
app.include_router(barapp)
app.include_router(vcardapp)
app.include_router(wifiapp)
app.include_router(tweetapp)
app.include_router(emailapp)
app.include_router(smsapp)
    

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8090, reload=True)