import os
import requests
from django.conf import settings
from django.urls import reverse
from urllib.parse import urljoin

CHAPA_BASE_URL = 'https://api.chapa.co/v1/'

def get_chapa_headers():
    """Get headers for Chapa API requests"""
    return {
        'Authorization': f'Bearer {os.getenv("CHAPA_SECRET_KEY")}',
        'Content-Type': 'application/json',
    }

def initialize_payment(amount, email, first_name, last_name, tx_ref, return_url, currency='ETB'):
    """Initialize payment with Chapa"""
    url = urljoin(CHAPA_BASE_URL, 'transaction/initialize')
    
    data = {
        'amount': str(amount),
        'currency': currency,
        'email': email,
        'first_name': first_name,
        'last_name': last_name,
        'tx_ref': tx_ref,
        'callback_url': return_url,
        'return_url': return_url,
    }
    
    try:
        response = requests.post(
            url,
            json=data,
            headers=get_chapa_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error initializing payment: {e}")
        return None

def verify_payment(transaction_reference):
    """Verify a payment with Chapa"""
    url = urljoin(CHAPA_BASE_URL, f'transaction/verify/{transaction_reference}')
    
    try:
        response = requests.get(
            url,
            headers=get_chapa_headers()
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error verifying payment: {e}")
        return None
