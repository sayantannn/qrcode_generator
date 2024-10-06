
from pydantic import BaseModel, Field


class SMSQRRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^\+?\d{10,15}$", description="Phone number must be a valid international format.")
    message: str = Field(None, max_length=160, description="SMS message cannot exceed 160 characters.")
    watermark_text: str = Field(None, max_length=100, description="Watermark text cannot exceed 100 characters.")