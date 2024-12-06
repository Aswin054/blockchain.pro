import requests

def get_transaction_data(address):
    url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}/full'
    response = requests.get(url)
    return response.json()

def monitor_transactions(addresses, threshold_amount=0.5):
    suspicious_transactions = []

    for address in addresses:
        data = get_transaction_data(address)
        if 'error' in data:
            print(f"Error fetching data for {address}: {data['error']}")
            continue

        for tx in data['txs']:
            tx_hash = tx['hash']
            total_amount = tx['total'] / 1e8  # Convert from satoshis to BTC
            fee_amount = tx['fee'] / 1e8 if 'fee' in tx else 0  # Handle fee if present

            # Flag suspicious transactions based on amount threshold
            if total_amount >= threshold_amount:
                suspicious_transactions.append({
                    'address': address,
                    'tx_hash': tx_hash,
                    'total_amount': total_amount,
                    'fee_amount': fee_amount,
                    'time': tx['received']
                })

    return suspicious_transactions

def display_suspicious_transactions(suspicious_transactions):
    if not suspicious_transactions:
        print("No suspicious transactions found.")
        return

    print(f"{'Address':<45} {'Transaction Hash':<66} {'Total Amount (BTC)':<20} {'Fee Amount (BTC)':<15} {'Time'}")
    print("=" * 200)

    for tx in suspicious_transactions:
        print(f"{tx['address']:<45} {tx['tx_hash']:<66} {tx['total_amount']:<20.8f} {tx['fee_amount']:<15.8f} {tx['time']}")

def display_hardcoded_suspicious_transactions():
    # Example of manually defined suspicious transactions
    suspicious_transactions = [
        {
            'address': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
            'tx_hash': '6cfe5cba59e42db54641f3b080b0c8ec41c0c2266243cccb9cfc9fcdcfba7035',
            'total_amount': 2.5,  # BTC
            'fee_amount': 0.0005,  # BTC
            'time': '2024-09-24 12:34:56'
        },
        {
            'address': '1EzwoHtiXB4iFwedPrRs8ePqSg1lL2y2LQ',
            'tx_hash': 'c3c0a678a1f54f6b9c82d0aade20821b8c1d8b75efb96d0a4e6856e1038c7491',
            'total_amount': 1.8,  # BTC
            'fee_amount': 0.0004,  # BTC
            'time': '2024-09-24 12:35:00'
        },
        {
            'address': '1BoW8dXY6K19AbKQZ4hA12P6Hg8czN7mTx',
            'tx_hash': 'f3f0e4e3f49f0a871cb3f7b74d7c8f0b1a6bce2d928e6b68574cb5a0c61d35c9',
            'total_amount': 0.9,  # BTC
            'fee_amount': 0.0001,  # BTC
            'time': '2024-09-24 12:36:12'
        },
    ]

    display_suspicious_transactions(suspicious_transactions)

def main():
    addresses = [
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Example Bitcoin address
        '1EzwoHtiXB4iFwedPrRs8ePqSg1lL2y2LQ',  # Add other addresses here
    ]
    threshold_amount = 0.5  # Set your threshold amount (in BTC)
    
    # Monitor transactions and display results
    suspicious_transactions = monitor_transactions(addresses, threshold_amount)
    display_suspicious_transactions(suspicious_transactions)

    # Display hardcoded suspicious transactions
    print("\nHardcoded Suspicious Transactions:")
    display_hardcoded_suspicious_transactions()

if __name__ == "__main__":
    main()
