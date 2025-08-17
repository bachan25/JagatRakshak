from twilio.rest import Client
import os
import urllib.parse  # to safely encode URL parameters

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_SID, TWILIO_TOKEN)

def make_call(phone_number: str, message: str):
    encoded_msg = urllib.parse.quote(message)
    dynamic_url = f"https://jagatrakshak.loca.lt/api/notify/twiml?msg={encoded_msg}"

    call = client.calls.create(
        to="+918018880648",
        from_=TWILIO_PHONE,
        url=dynamic_url,
        call_reason="Emergency Notification From JagatRakshak",  
        method="GET"
    )

    return call.sid
