from twilio.rest import Client
import os

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

def send_sms(phone_number: str, message: str):
    message = client.messages.create(
        to="+918018880648",
        from_=TWILIO_PHONE,
        body= message
    )
    return message.sid
