import requests
import pandas as pd

def get_blockchain_data(address):
    # Define the API endpoint
    url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}/full'

    try:
        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Check if there's an error in the response
        if 'error' in data:
            print(f"Error: {data['error']}")
            return None

        # Extract relevant information
        balance = data['final_balance'] / 1e8  # Convert satoshis to BTC
        tx_count = data['n_tx']
        transactions = data['txs']

        # Create a DataFrame for recent transactions
        tx_data = []
        for tx in transactions:
            tx_info = {
                'hash': tx['hash'],
                'block_height': tx['block_height'],
                'time': tx['received'],
                'total': tx['total'] / 1e8,  # Convert satoshis to BTC
                'fee': tx['fee'] / 1e8 if 'fee' in tx else 0,  # Handle fee if present
            }
            tx_data.append(tx_info)

        # Create a DataFrame from transaction data
        tx_df = pd.DataFrame(tx_data)

        # Display the results
        print(f"Address: {address}")
        print(f"Balance: {balance} BTC")
        print(f"Transaction Count: {tx_count}")
        print("\nRecent Transactions:")
        print(tx_df)

    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    # Replace with the Bitcoin address you want to analyze
    address = '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa'  # Example address
    get_blockchain_data(address)

if __name__ == "__main__":
    main()
