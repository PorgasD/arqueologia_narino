from twilio.rest import Client
from django.conf import settings

def send_verification_code(phone_number):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification = client.verify.services(settings.TWILIO_VERIFY_SID).verifications.create(
        to=phone_number,
        channel='sms'  # Puedes usar 'call' si prefieres llamadas
    )
    return verification.sid

def verify_code(phone_number, code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    verification_check = client.verify.services(settings.TWILIO_VERIFY_SID).verification_checks.create(
        to=phone_number,
        code=code
    )
    return verification_check.status == 'approved'