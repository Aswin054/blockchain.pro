import requests
import pandas as pd

def get_bitcoin_ethereum_data():
    try:
        # Define the API endpoint
        url = 'https://api.coingecko.com/api/v3/simple/price'
        
        # Define the parameters
        params = {
            'ids': 'bitcoin,ethereum',
            'vs_currencies': 'usd',
            'include_market_cap': 'true',
            'include_24hr_vol': 'true'
        }
        
        # Make the API request
        response = requests.get(url, params=params)
        data = response.json()
        
        # Print the full API response to check the structure
        print("Full API response:")
        print(data)

        # Extract relevant information
        bitcoin_data = {
            'currency': 'Bitcoin',
            'price_usd': data['bitcoin']['usd'],
            'market_cap_usd': data['bitcoin']['usd_market_cap'],
            '24hr_volume_usd': data['bitcoin']['usd_24h_vol']
        }

        ethereum_data = {
            'currency': 'Ethereum',
            'price_usd': data['ethereum']['usd'],
            'market_cap_usd': data['ethereum']['usd_market_cap'],
            '24hr_volume_usd': data['ethereum']['usd_24h_vol']
        }

        # Combine data into a DataFrame
        df = pd.DataFrame([bitcoin_data, ethereum_data])
        return df

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def main():
    transaction_data = get_bitcoin_ethereum_data()
    
    if transaction_data is not None:
        print(transaction_data)
    else:
        print("Failed to retrieve transaction data.")

if __name__ == "__main__":
    main()
