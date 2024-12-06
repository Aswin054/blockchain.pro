import pandas as pd
from datetime import datetime

# File path for storing reports
REPORTS_FILE = 'reports.csv'

# Initialize the reports DataFrame if it doesn't exist
try:
    reports_df = pd.read_csv(REPORTS_FILE)
except FileNotFoundError:
    reports_df = pd.DataFrame(columns=['report_id', 'address', 'tx_hash', 'total_amount', 'reported_by', 'notes', 'timestamp'])

def generate_report_id():
    return f"RPT-{len(reports_df) + 1:04d}"

def submit_report(address, tx_hash, total_amount, reported_by, notes=""):
    report_id = generate_report_id()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    new_report = pd.DataFrame([{
        'report_id': report_id,
        'address': address,
        'tx_hash': tx_hash,
        'total_amount': total_amount,
        'reported_by': reported_by,
        'notes': notes,
        'timestamp': timestamp
    }])
    
    global reports_df
    reports_df = pd.concat([reports_df, new_report], ignore_index=True)
    reports_df.to_csv(REPORTS_FILE, index=False)
    
    print(f"Report submitted successfully! Report ID: {report_id}")

def view_reports():
    if reports_df.empty:
        print("No reports available.")
        return
    
    print(reports_df[['report_id', 'address', 'tx_hash', 'total_amount', 'reported_by', 'timestamp']])

def add_note_to_report(report_id, note, added_by):
    global reports_df
    if report_id not in reports_df['report_id'].values:
        print(f"Report ID {report_id} not found.")
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    note_entry = f"{added_by} ({timestamp}): {note}"
    
    reports_df.loc[reports_df['report_id'] == report_id, 'notes'] += f"\n{note_entry}"
    reports_df.to_csv(REPORTS_FILE, index=False)
    
    print(f"Note added to Report ID {report_id}.")

def main():
    while True:
        print("\nUser Reporting and Collaboration System")
        print("1. Submit a Report")
        print("2. View All Reports")
        print("3. Add Note to a Report")
        print("4. Exit")
        
        choice = input("Select an option: ").strip()
        
        if choice == '1':
            address = input("Enter the Bitcoin Address: ").strip()
            tx_hash = input("Enter the Transaction Hash: ").strip()
            total_amount = float(input("Enter the Total Amount (BTC): ").strip())
            reported_by = input("Enter Your Name: ").strip()
            notes = input("Enter any notes (optional): ").strip()
            
            submit_report(address, tx_hash, total_amount, reported_by, notes)
        
        elif choice == '2':
            view_reports()
        
        elif choice == '3':
            report_id = input("Enter the Report ID: ").strip()
            note = input("Enter the note to add: ").strip()
            added_by = input("Enter Your Name: ").strip()
            
            add_note_to_report(report_id, note, added_by)
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
