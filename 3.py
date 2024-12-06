import requests
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def get_transaction_data(address):
    url = f'https://api.blockcypher.com/v1/btc/main/addrs/{address}/full'
    response = requests.get(url)
    return response.json()

def analyze_addresses(addresses):
    G = nx.DiGraph()  # Create a directed graph
    address_data = []

    for address in addresses:
        data = get_transaction_data(address)
        if 'error' in data:
            print(f"Error fetching data for {address}: {data['error']}")
            continue

        # Create nodes for the address and its transactions
        balance = data['final_balance'] / 1e8  # Convert from satoshis to BTC
        tx_count = data['n_tx']
        address_data.append((address, balance, tx_count))

        for tx in data['txs']:
            tx_hash = tx['hash']
            G.add_node(address)  # Add the address as a node
            G.add_node(tx_hash)  # Add the transaction as a node
            G.add_edge(address, tx_hash)  # Create an edge from the address to the transaction
            
            # Connect outputs to addresses receiving funds (if available)
            for output in tx.get('outputs', []):
                # Ensure 'addresses' exists and is a list
                if 'addresses' in output and isinstance(output['addresses'], list):
                    for recipient in output['addresses']:
                        G.add_node(recipient)
                        G.add_edge(tx_hash, recipient)  # Create an edge from the transaction to the recipient

    return G, address_data

def plot_graph(G):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G)  # Positioning for visualization
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='skyblue', font_size=10, font_weight='bold', arrows=True)
    plt.title("Blockchain Transaction Graph")
    plt.show()

def print_address_data(address_data):
    print(f"{'Address':<45} {'Balance (BTC)':<15} {'Transaction Count'}")
    print("=" * 75)
    for address, balance, tx_count in address_data:
        print(f"{address:<45} {balance:<15.8f} {tx_count}")

def main():
    addresses = [
        '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',  # Example Bitcoin address
        '1EzwoHtiXB4iFwedPrRs8ePqSg1lL2y2LQ',  # Add other addresses here
    ]
    graph, address_data = analyze_addresses(addresses)
    print_address_data(address_data)
    plot_graph(graph)

if __name__ == "__main__":
    main()
