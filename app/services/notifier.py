from twilio.rest import Client
from app.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def send_alert(to_number: str, message: str):
    client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_FROM,
        to=f"whatsapp:{to_number}"
    )
