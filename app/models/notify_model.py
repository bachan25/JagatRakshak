from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class SMSRequest(BaseModel):
    phone_number: str = Field(..., example="9876543210")
    message: str = Field(..., example="This is a notification message from JagatRakshak Emergency Response System.")

class EmailRequest(BaseModel):
    to: EmailStr = Field(..., example="alice@example.com")
    subject: str = Field(..., example="Emergency Alert")
    body: str = Field(..., example="This is a notification email from JagatRakshak Emergency Response System.")

class CallRequest(BaseModel):
    phone_number: str = Field(..., example="9876543210")
    message: Optional[str] = Field(..., example="This is a notification call from JagatRakshak Emergency Response System.")
