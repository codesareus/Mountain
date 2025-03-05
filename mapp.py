import requests
import pandas as pd
import streamlit as st
import datetime

# Schwab API details
CLIENT_ID = "your_api_key_here"
REDIRECT_URI = "your_redirect_uri_here"
REFRESH_TOKEN = "your_refresh_token_here"
ACCESS_TOKEN_URL = "https://api.schwabapi.com/v1/oauth2/token"
PRICE_HISTORY_URL = "https://api.schwabapi.com/v1/marketdata/{symbol}/pricehistory"

# Function to get access token
def get_access_token():
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': REFRESH_TOKEN,
        'client_id': CLIENT_ID
    }
    response = requests.post(ACCESS_TOKEN_URL, data=payload)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        st.error(f"Error fetching access token: {response.text}")
        return None
