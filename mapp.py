import streamlit as st
import requests
import webbrowser
import urllib.parse

# Schwab API credentials
CLIENT_ID = "fnB6k1X6JSFlQHravRt6T9m86AZlkD04"
#CLIENT_ID = "4nApHqYZJnYndGYnQxXGn4pAdxDQ48Gi"
CLIENT_SECRET = "3kBzb6yaQZ6tm3vM"
REDIRECT_URI = "https://developer.schwab.com/oauth2-redirect.html"  # Must match Schwab settings
AUTHORIZATION_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"

# Generate the login URL
params = {
    "response_type": "code",
    "client_id": CLIENT_ID,
    "scope": "readonly",  # Adjust scope if needed
    "redirect_uri": REDIRECT_URI,
}
auth_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(params)}"

st.title("Schwab API Authentication")

if st.button("Login to Schwab"):
    webbrowser.open(auth_url)  # Open login page in browser
    st.write(f"[Click here if it doesn't open automatically]({auth_url})")

auth_code = st.text_input("Paste the authorization code from the URL after login:")

def get_access_token(auth_code):
    payload = {
        "grant_type": "authorization_code",
        "code": auth_code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
    }
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    response = requests.post(TOKEN_URL, data=payload, headers=headers)
    
    if response.status_code == 200:
        token_data = response.json()
        st.success("Access token obtained!")
        st.write(token_data)  # Display token details (for debugging)
        return token_data.get("access_token")
    else:
        st.error(f"Error getting access token: {response.text}")
        return None

if auth_code and st.button("Get Access Token"):
    access_token = get_access_token(auth_code)

def get_price_history(symbol, access_token):
    url = f"https://api.schwabapi.com/v1/marketdata/{symbol}/pricehistory"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    params = {
        "periodType": "day",
        "period": 1,
        "frequencyType": "minute",
        "frequency": 1
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Error fetching price history: {response.text}")
        return None

# UI to enter stock symbol
symbol = st.text_input("Enter Stock Symbol (e.g., AAPL)")

if access_token and symbol and st.button("Fetch Price History"):
    data = get_price_history(symbol, access_token)
    if data:
        st.write(data)



