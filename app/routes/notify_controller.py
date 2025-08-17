from fastapi import APIRouter, HTTPException
from app.models.notify_model import SMSRequest, EmailRequest, CallRequest
from app.services.sms_service import send_sms
from app.services.email_service import send_email
from app.services.call_service import make_call
from fastapi.responses import Response
import xml.sax.saxutils as saxutils  # to escape special XML chars


router = APIRouter()

@router.post("/sms")
def notify_sms(req: SMSRequest):
    try:
        sid = send_sms(req.phone_number, req.message)
        return {"status": "success", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/email")
def notify_email(req: EmailRequest):
    try:
        print(f"Sending email to {req.to} with subject '{req.subject}'")
        print(f"Email body: {req.body}")
        result = send_email(req.to, req.subject, req.body)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/call")
def notify_call(req: CallRequest):
    try:
        sid = make_call(req.phone_number, req.message)
        return {"status": "success", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/twiml")   
def get_twiml(msg: str = "Hello! This is a default message."):
    escaped_msg = saxutils.escape(msg)  # Prevent XML injection

    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
        <Response>
            <Say voice="alice" language="en-IN">{escaped_msg}</Say>
        </Response>"""
        
    return Response(content=twiml, media_type="application/xml")



