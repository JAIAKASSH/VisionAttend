import requests
import os
from dotenv import load_dotenv

load_dotenv()

CALLMEBOT_API = "https://api.callmebot.com/whatsapp.php"
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER")
WHATSAPP_API_KEY = os.getenv("WHATSAPP_API_KEY")

def send_whatsapp_message(message):
    payload = {
        "phone": WHATSAPP_NUMBER,
        "apikey": WHATSAPP_API_KEY,
        "text": message
    }
    response = requests.get(CALLMEBOT_API, params=payload)
    if response.status_code == 200:
        print("[WHATSAPP] Message sent.")
    else:
        print("[WHATSAPP] Failed to send.", response.text)