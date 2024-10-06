from pydantic import BaseModel, EmailStr


class VCardData(BaseModel):
    name: str               
    Firstname: str
    Lastname: str
    mobile: str
    phone: str = None
    fax: str = None
    email: EmailStr
    company: str = None
    job: str = None
    street: str = None
    city: str = None
    zip: str = None
    state: str = None
    country: str = None
    website: str = None