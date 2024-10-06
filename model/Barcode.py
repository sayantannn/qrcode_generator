from pydantic import BaseModel


class BarcodeType(BaseModel):
    code: str
    name: str