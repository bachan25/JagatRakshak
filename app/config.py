import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_FROM = os.getenv("TWILIO_WHATSAPP_FROM")
TWILIO_SMS_FROM = os.getenv("TWILIO_SMS_FROM")
EMERGENCY_CONTACTS = {
    "fire": os.getenv("EMERGENCY_CONTACT_FIRE"),
    "police": os.getenv("EMERGENCY_CONTACT_POLICE"),
    "ambulance": os.getenv("EMERGENCY_CONTACT_AMBULANCE"),
}
