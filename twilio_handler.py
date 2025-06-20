import os
from twilio.rest import Client
from flask import request, Response
from dotenv import load_dotenv
import openai
from rag import ProductRAG

from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

print("TWILIO_ACCOUNT_SID:", os.getenv('TWILIO_ACCOUNT_SID'))
print("TWILIO_AUTH_TOKEN:", os.getenv('TWILIO_AUTH_TOKEN'))
print("TWILIO_PHONE_NUMBER:", os.getenv('TWILIO_PHONE_NUMBER'))

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
rag = ProductRAG()

COUPON_CODE = "SAVE10"

def initiate_call(customer_phone, customer_name, cart_items):
    call = client.calls.create(
        to=customer_phone,
        from_=TWILIO_PHONE_NUMBER,
        url="https://randomstring.trycloudflare.com/voice/entry"
    )
    return call.sid

from flask import Blueprint
voice_bp = Blueprint('voice', __name__)

@voice_bp.route('/voice/entry', methods=['POST'])
def voice_entry():
    response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Test-User">Hi! This is your store calling about your recent cart. You left some great products behind. As a thank you, here is a coupon code: {COUPON_CODE} for 10% off. Would you like to hear more about any product or need help completing your purchase? Please say your question after the beep.</Say>
    <Record action="/voice/handle_query" maxLength="10" playBeep="true" />
</Response>'''
    return Response(response, mimetype='text/xml')


@voice_bp.route('/voice/handle_query', methods=['POST'])
def handle_query():
    recording_url = request.form.get('RecordingUrl')
    user_query = "What is special about the smart watch?" 
    answer = rag.answer_query(user_query)
    response = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Test-User">{answer} Would you like to proceed to checkout? Say yes to get a payment link, or ask another question.</Say>
    <Record action="/voice/handle_query" maxLength="10" playBeep="true" />
</Response>'''
    return Response(response, mimetype='text/xml') 