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

# Upload CSV functionality
def upload_transaction_data():
    st.title("Upload Transaction Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.write(df)
        return df
    else:
        st.write("Please upload a CSV file to proceed.")
        return None

# Transaction Data Collection (from uploaded CSV)
def collect_transaction_data(df):
    st.write("Uploaded Transaction Data:")
    st.write(df)

# Blockchain Analysis
def analyze_blockchain(df):
    st.write("Analyzing blockchain data (example: counting transactions by type)...")
    st.write(df.groupby('transaction_type').size().reset_index(name='counts'))

# Anonymity and Pseudonymity
def analyze_anonymity_pseudonymity(df):
    st.write("Analyzing anonymity and pseudonymity (example: display addresses)...")
    unique_addresses = df['address'].unique()
    st.write(unique_addresses)

# Transaction Monitoring
def monitor_transactions(df):
    st.write("Monitoring transactions (highlighting suspicious and fraudulent transactions)...")
    
    # Displaying entire data
    st.subheader("Entire Transaction Data")
    st.write(df)
    
    # Displaying fraudulent transactions separately
    st.subheader("Fraudulent Transactions")
    fraudulent = df[df['is_fraudulent']]
    st.write(fraudulent)

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
    transaction_counts = df['transaction_type'].value_counts().reset_index()
    transaction_counts.columns = ['transaction_type', 'count']
    
    fig = px.pie(transaction_counts, values='count', names='transaction_type', title='Transaction Type Proportions')
    st.plotly_chart(fig)

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
    
    report.drawString(100, 600, 'Transaction Details:')
    text = report.beginText(100, 580)
    text.setFont('Helvetica', 10)
    for index, row in df.iterrows():
        text.textLine(f"ID: {row['transaction_id']}, Type: {row['transaction_type']}, Amount: ${row['amount']}, Status: {row['status']}, Fraudulent: {row['is_fraudulent']}, Date: {row['timestamp']}")
    report.drawText(text)
    
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
    st.write("Counting peer-to-peer transactions...")
    peer_count = df.groupby(['address', 'recipient']).size().reset_index(name='transaction_count')
    st.write(peer_count)

# Simulate Peer-to-Peer Transactions
def simulate_transactions(df):
    st.write("Simulating new peer-to-peer transactions...")
    
    # Number of new transactions to simulate
    num_transactions = st.slider("Number of transactions to simulate", 1, 100, 10)
    
    # Simulate transactions
    addresses = df['address'].unique()
    recipients = df['recipient'].unique()
    
    new_transactions = []
    for _ in range(num_transactions):
        address = random.choice(addresses)
        recipient = random.choice(recipients)
        amount = round(random.uniform(1, 1000), 2)  # Random transaction amount
        is_fraudulent = random.choice([True, False])  # Random fraudulent flag
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
    
    # Add the new transactions to the existing DataFrame
    new_df = pd.DataFrame(new_transactions)
    updated_df = pd.concat([df, new_df], ignore_index=True)
    
    st.write("Updated Transaction Data with Simulated Transactions:")
    st.write(updated_df)
    
    return updated_df

# Enhanced 3D Visualization of Blockchain Connections
def visualize_blockchain_network(df):
    st.write("3D Visualization of Blockchain Connections with Fraudulent Transactions Highlighted")
    
    # Creating a graph using networkx
    G = nx.Graph()

    for i, row in df.iterrows():
        G.add_edge(row['address'], row['recipient'], weight=row['amount'], fraudulent=row['is_fraudulent'])

    # Prepare edge data for Plotly
    edge_x = []
    edge_y = []
    colors = []
    
    for edge in G.edges(data=True):
        x0, y0 = np.random.rand(2)
        x1, y1 = np.random.rand(2)
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        
        # Color edges based on fraudulent status
        if edge[2]['fraudulent']:
            colors.append('red')
        else:
            colors.append('black')
    
    edge_traces = []
    for i in range(len(edge_x) // 3):
        trace = go.Scatter(
            x=edge_x[i*3:i*3+3],
            y=edge_y[i*3:i*3+3],
            line=dict(width=2, color=colors[i]),  # Different color for each edge
            hoverinfo='none',
            mode='lines'
        )
        edge_traces.append(trace)

    fig = go.Figure(data=edge_traces)
    
    fig.update_layout(
        title="Blockchain Connections in 3D",
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=False),
        showlegend=False,
        height=700
    )
    
    st.plotly_chart(fig)

# Alternative Enhanced 3D Visualization
def visualize_blockchain_connections_3D(df):
    st.write("Alternative 3D Visualization of Blockchain Connections with Fraudulent Transactions Highlighted")
    
    colors = df['is_fraudulent'].map({True: 'red', False: 'blue'})
    
    fig = go.Figure()

    # Creating 3D scatter plot for addresses (clients) and recipients (servers)
    fig.add_trace(go.Scatter3d(
        x=np.random.rand(len(df)),
        y=np.random.rand(len(df)),
        z=df['amount'],
        mode='markers',
        marker=dict(size=8, color=colors, opacity=0.8),
        text=df.apply(lambda row: f"Type: {row['transaction_type']}<br>Amount: {row['amount']}<br>Fraudulent: {row['is_fraudulent']}", axis=1)
    ))

    fig.update_layout(
        scene=dict(
            xaxis_title='Client (Address)',
            yaxis_title='Server (Recipient)',
            zaxis_title='Transaction Amount',
            xaxis=dict(backgroundcolor="rgb(200, 200, 230)"),
            yaxis=dict(backgroundcolor="rgb(230, 200, 200)"),
            zaxis=dict(backgroundcolor="rgb(200, 230, 200)")
        ),
        title="Blockchain Connections in 3D",
        margin=dict(l=0, r=0, b=0, t=40),
        height=700
    )

    st.plotly_chart(fig)

# Streamlit Sidebar for Navigation
st.sidebar.title("Blockchain Analysis Tool")
options = ["Upload Transaction Data", "Blockchain Analysis", "Anonymity and Pseudonymity", 
           "Transaction Monitoring", "User Reporting and Collaboration", "Data Privacy and Security", 
           "Visualization and Reporting Tools", "Peer-to-Peer Transaction Count", 
           "Simulate Transactions", "3D Visualization of Blockchain"]

choice = st.sidebar.selectbox("Choose an option", options)

if choice == "Upload Transaction Data":
    df = upload_transaction_data()
    if df is not None:
        collect_transaction_data(df)
elif choice == "Blockchain Analysis":
    df = upload_transaction_data()
    if df is not None:
        analyze_blockchain(df)
elif choice == "Anonymity and Pseudonymity":
    df = upload_transaction_data()
    if df is not None:
        analyze_anonymity_pseudonymity(df)
elif choice == "Transaction Monitoring":
    df = upload_transaction_data()
    if df is not None:
        monitor_transactions(df)
elif choice == "User Reporting and Collaboration":
    user_reporting_collaboration()
elif choice == "Data Privacy and Security":
    data_privacy_security()
elif choice == "Visualization and Reporting Tools":
    df = upload_transaction_data()
    if df is not None:
        visualization_reporting_tools(df)
elif choice == "Peer-to-Peer Transaction Count":
    df = upload_transaction_data()
    if df is not None:
        peer_to_peer_transaction_count(df)
elif choice == "Simulate Transactions":
    df = upload_transaction_data()
    if df is not None:
        updated_df = simulate_transactions(df)
elif choice == "3D Visualization of Blockchain":
    df = upload_transaction_data()
    if df is not None:
        visualize_blockchain_connections_3D(df)
