import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EBAY_APP_ID")
CLIENT_SECRET = os.getenv("EBAY_CERT_ID")

def get_application_token():
    # eBay Sandbox Token Endpoint
    url = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    
    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    return response.json()

if __name__ == "__main__":
    print("Testing eBay Sandbox Authentication...")
    token_data = get_application_token()
    print(token_data)