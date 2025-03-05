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

def get_price_history(symbol, period='1d', frequency='minute'):
    access_token = get_access_token()
    if not access_token:
        return None
    
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "apikey": CLIENT_ID,
        "periodType": "day",
        "period": 1,
        "frequencyType": "minute",
        "frequency": 1
    }
    
    response = requests.get(PRICE_HISTORY_URL.format(symbol=symbol), headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return data.get("candles", [])
    else:
        st.error(f"Error fetching price history: {response.text}")
        return None


st.title("Schwab Stock Price History")

symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)", "AAPL")

if st.button("Fetch Price History"):
    data = get_price_history(symbol)
    
    if data:
        df = pd.DataFrame(data)
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        st.write(df)
        st.line_chart(df.set_index("datetime")["close"])
    else:
        st.warning("No data found!")
