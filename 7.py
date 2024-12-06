import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

# Sample data for transactions
data = {
    'transaction_id': [1, 2, 3, 4, 5, 6],
    'timestamp': ['2024-09-01', '2024-09-02', '2024-09-03', '2024-09-04', '2024-09-05', '2024-09-06'],
    'amount': [1000, 1500, 700, 1200, 1300, 900],
    'transaction_type': ['BTC', 'ETH', 'BTC', 'ETH', 'BTC', 'ETH'],
    'status': ['completed', 'pending', 'completed', 'completed', 'failed', 'completed']
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Convert 'timestamp' to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Function to visualize transaction trends
def visualize_transaction_trends(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x='timestamp', y='amount', hue='transaction_type', data=df, marker='o')
    plt.title('Transaction Trends Over Time')
    plt.xlabel('Timestamp')
    plt.ylabel('Amount ($)')
    plt.grid(True)
    plt.show()

# Function to visualize transaction amount distribution
def visualize_transaction_distribution(df):
    plt.figure(figsize=(8, 5))
    sns.barplot(x='transaction_type', y='amount', hue='status', data=df)
    plt.title('Transaction Amount Distribution')
    plt.xlabel('Transaction Type')
    plt.ylabel('Amount ($)')
    plt.grid(True)
    plt.show()

# Updated Function to visualize transaction type proportions
def visualize_transaction_proportions(df):
    transaction_counts = df['transaction_type'].value_counts().reset_index()
    transaction_counts.columns = ['transaction_type', 'count']
    
    fig = px.pie(transaction_counts, values='count', names='transaction_type', title='Transaction Type Proportions')
    fig.show()

# Function to generate a simple PDF report
def generate_report(df, filename='transaction_report.pdf'):
    report = canvas.Canvas(filename, pagesize=letter)
    report.setTitle('Transaction Report')
    
    # Title
    report.setFont('Helvetica-Bold', 16)
    report.drawString(100, 750, 'Transaction Report')

    # Summary
    total_transactions = len(df)
    completed_transactions = df[df['status'] == 'completed'].shape[0]
    pending_transactions = df[df['status'] == 'pending'].shape[0]
    failed_transactions = df[df['status'] == 'failed'].shape[0]
    
    report.setFont('Helvetica', 12)
    report.drawString(100, 700, f'Total Transactions: {total_transactions}')
    report.drawString(100, 680, f'Completed Transactions: {completed_transactions}')
    report.drawString(100, 660, f'Pending Transactions: {pending_transactions}')
    report.drawString(100, 640, f'Failed Transactions: {failed_transactions}')
    
    # Detailed table
    report.drawString(100, 600, 'Transaction Details:')
    text = report.beginText(100, 580)
    text.setFont('Helvetica', 10)
    for index, row in df.iterrows():
        text.textLine(f"ID: {row['transaction_id']}, Type: {row['transaction_type']}, Amount: ${row['amount']}, Status: {row['status']}, Date: {row['timestamp'].strftime('%Y-%m-%d')}")
    report.drawText(text)
    
    # Save the PDF
    report.save()
    print(f'Report saved as {filename}')

# Main function to run the visualizations and generate the report
def main():
    print("Visualizing Transaction Trends...")
    visualize_transaction_trends(df)
    
    print("Visualizing Transaction Distribution...")
    visualize_transaction_distribution(df)
    
    print("Visualizing Transaction Proportions...")
    visualize_transaction_proportions(df)
    
    print("Generating Report...")
    generate_report(df)

if __name__ == "__main__":
    main()
