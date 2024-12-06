import pandas as pd
import numpy as np

# Seed for reproducibility
np.random.seed(42)

# Define the parameters for the synthetic data
num_records = 10000
transaction_types = ['BTC', 'ETH', 'LTC', 'XRP']  # Bitcoin, Ethereum, Litecoin, Ripple
addresses = [f'addr{i}' for i in range(1, num_records + 1)]
recipients = [f'rec{i}' for i in range(1, num_records + 1)]
status_options = ['completed', 'pending', 'failed']

# Generate synthetic data
data = {
    'transaction_id': np.arange(1, num_records + 1),
    'timestamp': pd.date_range(start='2024-01-01', periods=num_records, freq='T'),
    'amount': np.random.randint(100, 2000, size=num_records),
    'transaction_type': np.random.choice(transaction_types, size=num_records),
    'status': np.random.choice(status_options, size=num_records),
    'address': np.random.choice(addresses, size=num_records),
    'recipient': np.random.choice(recipients, size=num_records),
    'is_fraudulent': np.random.choice([True, False], size=num_records, p=[0.05, 0.95])  # 5% marked as fraudulent
}

# Convert the data into a DataFrame
df = pd.DataFrame(data)

# Display the first few rows of the generated data
print(df.head())

# Optionally, save to a CSV file
df.to_csv("synthetic_transaction_data.csv", index=False)
