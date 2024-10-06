from pydantic import BaseModel, EmailStr, Field


class EmailQRRequest(BaseModel):
    email: EmailStr
    subject: str = Field(None, max_length=255, description="Email subject cannot exceed 255 characters.")
    message: str = Field(None, max_length=1000, description="Email message cannot exceed 1000 characters.")
    watermark_text: str = Field(None, max_length=100, description="Watermark text cannot exceed 100 characters.")
