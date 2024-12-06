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

# Upload CSV functionality with error handling
def upload_transaction_data():
    st.title("Upload Transaction Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("Data loaded successfully!")
            st.write(df.head())  # Display first few rows to confirm structure
            return df
        except Exception as e:
            st.error(f"Error reading the file: {e}")
            return None
    else:
        st.write("Please upload a CSV file to proceed.")
        return None

# Transaction Data Collection (from uploaded CSV)
def collect_transaction_data(df):
    if df is not None:
        st.write("Uploaded Transaction Data:")
        st.write(df)
    else:
        st.warning("No data to display. Please upload a valid CSV file.")

# Blockchain Analysis
def analyze_blockchain(df):
    if df is not None:
        st.write("Analyzing blockchain data (example: counting transactions by type)...")
        try:
            st.write(df.groupby('transaction_type').size().reset_index(name='counts'))
        except Exception as e:
            st.error(f"Error analyzing blockchain: {e}")
    else:
        st.warning("No data to analyze. Please upload a valid CSV file.")

# Anonymity and Pseudonymity
def analyze_anonymity_pseudonymity(df):
    if df is not None:
        st.write("Analyzing anonymity and pseudonymity (example: display addresses)...")
        try:
            unique_addresses = df['address'].unique()
            st.write(unique_addresses)
        except KeyError as e:
            st.error(f"Missing column for analysis: {e}")
    else:
        st.warning("No data to analyze. Please upload a valid CSV file.")

# Transaction Monitoring
def monitor_transactions(df):
    if df is not None:
        st.write("Monitoring transactions (highlighting suspicious and fraudulent transactions)...")
        st.subheader("Entire Transaction Data")
        st.write(df)
        
        st.subheader("Fraudulent Transactions")
        fraudulent = df[df['is_fraudulent']]
        st.write(fraudulent)
    else:
        st.warning("No data to monitor. Please upload a valid CSV file.")

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
    if df is not None:
        transaction_counts = df['transaction_type'].value_counts().reset_index()
        transaction_counts.columns = ['transaction_type', 'count']
        
        fig = px.pie(transaction_counts, values='count', names='transaction_type', title='Transaction Type Proportions')
        st.plotly_chart(fig)
    else:
        st.warning("No data to visualize. Please upload a valid CSV file.")

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
    if df is not None:
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
    else:
        st.warning("No data to visualize or generate a report. Please upload a valid CSV file.")

# Peer-to-Peer Transaction Count
def peer_to_peer_transaction_count(df):
    if df is not None:
        st.write("Counting peer-to-peer transactions...")
        peer_count = df.groupby(['address', 'recipient']).size().reset_index(name='transaction_count')
        st.write(peer_count)
    else:
        st.warning("No data to count. Please upload a valid CSV file.")

# Simulate Peer-to-Peer Transactions
def simulate_transactions(df):
    if df is not None:
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
        st.warning("No data to simulate transactions. Please upload a valid CSV file.")

# Main function
def main():
    df = upload_transaction_data()
    
    if df is not None:
        collect_transaction_data(df)
        analyze_blockchain(df)
        analyze_anonymity_pseudonymity(df)
        monitor_transactions(df)
        user_reporting_collaboration()
        data_privacy_security()
        visualization_reporting_tools(df)
        peer_to_peer_transaction_count(df)
        simulate_transactions(df)
    else:
        st.warning("No data available. Please upload a CSV file.")

if __name__ == "__main__":
    main()
