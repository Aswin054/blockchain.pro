import requests

def get_block_info(hash_id):
    """
    Fetch block information using Blockchain.com API.
    
    Args:
        hash_id (str): Block hash to query.
        
    Returns:
        dict: Block information if the request is successful.
    """
    API_URL = f"https://blockchain.info/rawblock/{hash_id}"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        block_info = response.json()

        # Print key block details
        print("\n--- Block Information ---")
        print(f"Hash: {block_info.get('hash')}")
        print(f"Height: {block_info.get('height')}")
        print(f"Time: {block_info.get('time')}")
        print(f"Block Size: {block_info.get('size')} bytes")
        print(f"Number of Transactions: {len(block_info.get('tx', []))}")

        return block_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching block data: {e}")
        return None

def get_transaction_details(tx_id):
    """
    Fetch transaction details using Blockchain.com API.
    
    Args:
        tx_id (str): Transaction ID to query.
        
    Returns:
        dict: Transaction details if the request is successful.
    """
    API_URL = f"https://blockchain.info/rawtx/{tx_id}"

    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        transaction_info = response.json()

        # Display key transaction details
        print("\n--- Transaction Details ---")
        print(f"Transaction Hash: {transaction_info.get('hash')}")
        print("Inputs:")
        for tx_input in transaction_info.get("inputs", []):
            prev_out = tx_input.get("prev_out", {})
            address = prev_out.get("addr", "N/A")
            print(f"  - From: {address}")
        print("Outputs:")
        for tx_output in transaction_info.get("out", []):
            address = tx_output.get("addr", "N/A")
            value_btc = tx_output.get("value", 0) / 1e8  # Convert Satoshis to BTC
            print(f"  - To: {address}, Value: {value_btc} BTC")

        return transaction_info

    except requests.exceptions.RequestException as e:
        print(f"Error fetching transaction details: {e}")
        return None

def visualize_transactions(block_data):
    """
    Visualize all transactions in a block by fetching and displaying details.
    
    Args:
        block_data (dict): Block information containing transactions.
    """
    transactions = block_data.get("tx", [])
    if not transactions:
        print("No transactions found in this block.")
        return

    print(f"\n--- Visualizing Transactions in Block ---")
    for i, tx in enumerate(transactions[:5], start=1):  # Limit to first 5 transactions for simplicity
        tx_id = tx.get("hash")
        print(f"\nTransaction {i}: {tx_id}")
        transaction_details = get_transaction_details(tx_id)
        if not transaction_details:
            print("Failed to fetch details for this transaction.")

if __name__ == "__main__":
    # Replace with a valid block hash
    block_hash = input("Enter the block hash ID: ").strip()

    if block_hash:
        block_data = get_block_info(block_hash)
        if block_data:
            print("\nBlock data retrieved successfully!")
            visualize_transactions(block_data)
        else:
            print("Failed to retrieve block data.")
    else:
        print("No block hash ID provided.")
