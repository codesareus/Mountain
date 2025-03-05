import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

# Set up the Streamlit page
st.title("Charles Schwab Price History App")

# Input for API Key (use Streamlit secrets for better security)
api_key = st.text_input("Enter your API Key:", type="password")

# User inputs
symbol = st.text_input("Enter a stock symbol (e.g., AAPL):", "AAPL")
start_date = st.date_input("Start date:")
end_date = st.date_input("End date:")

if st.button("Fetch Price History"):
    if not api_key:
        st.error("Please enter your API key.")
    else:
        # Replace with Schwab's actual API endpoint (hypothetical example)
        url = "https://api.schwab.com/marketdata/v1"
        
        # Parameters (adjust based on Schwab's API requirements)
        params = {
            "symbol": symbol,
            "from": start_date.strftime("%Y-%m-%d"),
            "to": end_date.strftime("%Y-%m-%d"),
            "apikey": "4nApHqYZJnYndGYnQxXGn4pAdxDQ48Gi",
            "resolution": "D"  # Daily data
        }

        # Headers (if required)
        headers = {
            "Accept": "application/json"
        }

        try:
            response = requests.get(url, params=params, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Convert to DataFrame (adjust based on the API response structure)
                # Hypothetical example:
                df = pd.DataFrame(data["candles"])
                df["datetime"] = pd.to_datetime(df["datetime"], unit="ms")  # Convert epoch to datetime
                df.set_index("datetime", inplace=True)

                # Display data
                st.subheader(f"Price History for {symbol}")
                st.dataframe(df)

                # Plot closing prices
                st.subheader("Closing Prices Over Time")
                fig, ax = plt.subplots()
                ax.plot(df.index, df["close"], label="Close Price")
                ax.set_xlabel("Date")
                ax.set_ylabel("Price (USD)")
                ax.legend()
                st.pyplot(fig)

            else:
                st.error(f"API request failed: {response.status_code} - {response.text}")
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
