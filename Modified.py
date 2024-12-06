import pandas as pd
import plotly.express as px
import streamlit as st
import numpy as np
from cryptography.fernet import Fernet
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import plotly.graph_objects as go
import networkx as nx
import random
from datetime import datetime
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Upload CSV functionality
def upload_transaction_data():
    st.title("Upload Transaction Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write("Uploaded Data:")
        st.write(df)
        return df
    else:
        st.warning("Please upload a CSV file to proceed.")
        return None

# Transaction Data Collection
def collect_transaction_data(df):
    st.write("Uploaded Transaction Data:")
    st.write(df)

# Blockchain Analysis
def analyze_blockchain(df):
    if 'transaction_type' in df.columns:
        st.write("Analyzing blockchain data (example: counting transactions by type)...")
        transaction_counts = df.groupby('transaction_type').size().reset_index(name='counts')
        st.write(transaction_counts)
    else:
        st.warning("The 'transaction_type' column is missing from the uploaded data.")

# Anonymity and Pseudonymity
def analyze_anonymity_pseudonymity(df):
    if 'address' in df.columns:
        st.write("Analyzing anonymity and pseudonymity (example: display addresses)...")
        unique_addresses = df['address'].unique()
        st.write(unique_addresses)
    else:
        st.warning("The 'address' column is missing from the uploaded data.")

# Fraud Detection Using Isolation Forest
def fraud_detection(df):
    st.write("Detecting suspicious and fraudulent transactions using machine learning...")

    if 'amount' in df.columns:
        scaler = StandardScaler()
        df['amount_scaled'] = scaler.fit_transform(df[['amount']])
        model = IsolationForest(contamination=0.05, random_state=42)
        df['fraud_prediction'] = model.fit_predict(df[['amount_scaled']])
        df['is_suspicious'] = df['fraud_prediction'] == -1
        st.write("Flagged Suspicious Transactions:")
        st.write(df[df['is_suspicious']])
        return df
    else:
        st.warning("The 'amount' column is missing from the uploaded data.")
        return df

# Transaction Monitoring
def monitor_transactions(df):
    st.write("Monitoring transactions (highlighting suspicious and fraudulent transactions)...")
    if 'is_suspicious' in df.columns:
        st.subheader("Entire Transaction Data")
        st.write(df)

        st.subheader("Flagged Fraudulent Transactions")
        fraudulent = df[df['is_suspicious']]
        st.write(fraudulent)
    else:
        st.warning("Suspicious transactions have not been flagged. Please run fraud detection first.")

# User Reporting and Collaboration
def submit_report(transaction_id, reported_by, notes):
    report = {
        "transaction_id": transaction_id,
        "reported_by": reported_by,
        "notes": notes
    }
    st.write("Report submitted:", report)

def user_reporting_collaboration():
    st.write("User Reporting and Collaboration")
    transaction_id = st.text_input("Transaction ID")
    reported_by = st.text_input("Reported By")
    notes = st.text_area("Notes")

    if st.button("Submit Report"):
        submit_report(transaction_id, reported_by, notes)

# Data Privacy and Security
def encrypt_data(key, data):
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode())
    return encrypted_data

def decrypt_data(key, encrypted_data):
    fernet = Fernet(key)
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    return decrypted_data

def data_privacy_security():
    st.write("Data Privacy and Security")
    key = Fernet.generate_key()
    st.write("Encryption Key:", key.decode())

    data_to_encrypt = st.text_input("Data to Encrypt")
    if st.button("Encrypt Data"):
        encrypted_data = encrypt_data(key, data_to_encrypt)
        st.write("Encrypted Data:", encrypted_data.decode())
        if st.button("Decrypt Data"):
            decrypted_data = decrypt_data(key, encrypted_data)
            st.write("Decrypted Data:", decrypted_data)

# Visualization and Reporting Tools
def visualize_transaction_proportions(df):
    if 'transaction_type' in df.columns:
        transaction_counts = df['transaction_type'].value_counts().reset_index()
        transaction_counts.columns = ['transaction_type', 'count']

        fig = px.pie(transaction_counts, values='count', names='transaction_type', title='Transaction Type Proportions')
        st.plotly_chart(fig)
    else:
        st.warning("The 'transaction_type' column is missing from the uploaded data.")

def generate_report(df):
    buffer = BytesIO()
    report = canvas.Canvas(buffer, pagesize=letter)
    report.setTitle('Transaction Report')

    report.setFont('Helvetica-Bold', 16)
    report.drawString(100, 750, 'Transaction Report')

    total_transactions = len(df)
    completed_transactions = df[df['status'] == 'completed'].shape[0]
    pending_transactions = df[df['status'] == 'pending'].shape[0]
    failed_transactions = df[df['status'] == 'failed'].shape[0]

    report.setFont('Helvetica', 12)
    report.drawString(100, 700, f'Total Transactions: {total_transactions}')
    report.drawString(100, 680, f'Completed Transactions: {completed_transactions}')
    report.drawString(100, 660, f'Pending Transactions: {pending_transactions}')
    report.drawString(100, 640, f'Failed Transactions: {failed_transactions}')

    report.save()
    buffer.seek(0)
    return buffer

def visualization_reporting_tools(df):
    st.write("Visualization and Reporting Tools")

    visualize_transaction_proportions(df)

    if st.button("Generate PDF Report"):
        report_buffer = generate_report(df)
        st.download_button(
            label="Download Report as PDF",
            data=report_buffer,
            file_name="transaction_report.pdf",
            mime="application/pdf"
        )

# Peer-to-Peer Transaction Count
def peer_to_peer_transaction_count(df):
    if 'address' in df.columns and 'recipient' in df.columns:
        st.write("Counting peer-to-peer transactions...")
        peer_count = df.groupby(['address', 'recipient']).size().reset_index(name='transaction_count')
        st.write(peer_count)
    else:
        st.warning("Required columns 'address' and 'recipient' are missing.")

# Simulate Peer-to-Peer Transactions
def simulate_transactions(df):
    if 'address' in df.columns and 'recipient' in df.columns:
        st.write("Simulating new peer-to-peer transactions...")

        num_transactions = st.slider("Number of transactions to simulate", 1, 100, 10)
        addresses = df['address'].unique()
        recipients = df['recipient'].unique()

        new_transactions = []
        for _ in range(num_transactions):
            address = random.choice(addresses)
            recipient = random.choice(recipients)
            amount = round(random.uniform(1, 1000), 2)
            is_fraudulent = random.choice([True, False])
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            new_transaction = {
                'transaction_id': f"T{random.randint(10000, 99999)}",
                'address': address,
                'recipient': recipient,
                'transaction_type': 'peer-to-peer',
                'amount': amount,
                'is_fraudulent': is_fraudulent,
                'timestamp': timestamp,
                'status': 'completed'
            }
            new_transactions.append(new_transaction)

        new_df = pd.DataFrame(new_transactions)
        updated_df = pd.concat([df, new_df], ignore_index=True)

        st.write("Updated Transaction Data with Simulated Transactions:")
        st.write(updated_df)

        return updated_df
    else:
        st.warning("Required columns 'address' and 'recipient' are missing.")
        return df

# Neuron-Like 3D Visualization of Blockchain Connections (Fraudulent Transactions Only)
def visualize_neuron_like_blockchain_network(df):
    if 'is_suspicious' in df.columns:
        st.write("3D Neuron-Like Visualization of Blockchain Connections with Fraudulent Transactions Highlighted")

        # Filter fraudulent transactions
        fraudulent_df = df[df['is_suspicious']]

        # Create a NetworkX graph
        G = nx.Graph()

        # Add nodes and edges from the DataFrame
        for i, row in fraudulent_df.iterrows():
            G.add_node(row['address'])
            G.add_node(row['recipient'])
            G.add_edge(row['address'], row['recipient'], weight=row['amount'], fraudulent=row['is_suspicious'])

        # Generate random 3D positions for each node
        pos = {node: (np.random.uniform(-1, 1), np.random.uniform(-1, 1), np.random.uniform(-1, 1)) for node in G.nodes()}

        # Extract edges with fraudulent information
        edge_x, edge_y, edge_z = [], [], []
        for edge in G.edges(data=True):
            x0, y0, z0 = pos[edge[0]]
            x1, y1, z1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            edge_z.extend([z0, z1, None])

        # Create 3D plot for the edges
        fig = go.Figure(data=[go.Scatter3d(
            x=edge_x,
            y=edge_y,
            z=edge_z,
            mode='lines',
            line=dict(color='black', width=2)
        )])

        # Add nodes to the plot
        node_x, node_y, node_z = zip(*pos.values())
        fig.add_trace(go.Scatter3d(
            x=node_x,
            y=node_y,
            z=node_z,
            mode='markers',
            marker=dict(size=6, color='red', symbol='circle')
        ))

        fig.update_layout(title="Blockchain Neuron-Like Visualization", showlegend=False)
        st.plotly_chart(fig)
    else:
        st.warning("Fraudulent transaction data not available. Please run fraud detection first.")

# Main function to run the Streamlit app
def main():
    df = upload_transaction_data()

    if df is not None:
        collect_transaction_data(df)
        analyze_blockchain(df)
        analyze_anonymity_pseudonymity(df)
        df = fraud_detection(df)
        monitor_transactions(df)
        user_reporting_collaboration()
        data_privacy_security()
        visualization_reporting_tools(df)
        peer_to_peer_transaction_count(df)
        df = simulate_transactions(df)
        visualize_neuron_like_blockchain_network(df)

if __name__ == '__main__':
    main()
