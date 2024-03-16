import csv
import numpy as np

def clean_data(input_file, output_file):
    cleaned_data = []

    with open(input_file, 'r') as csvfile:
        reader = csv.reader(csvfile)

        # Skip header
        next(reader)

        for row in reader:
             # Correct OCR-like errors in account numbers only
            if row[1] not in ['SUBTOTAL', 'YEARLY TOTAL']:
                account_number = row[1].replace('O', '0').replace('o', '0').replace('l', '1').replace('I', '1')
            else:
                account_number = row[1]

            # Normalize amount values to a consistent format
            amount_str = row[3].replace('$', '').replace(',', '')
            amount = float(amount_str) if '.' in amount_str else int(amount_str)

            # Handle negative values for withdrawals
            if 'Withdrawal' in row[2]:
                amount *= -1

            cleaned_row = [row[0], account_number, row[2], amount, row[4]]
            cleaned_data.append(cleaned_row)

    # Write cleaned data to output file
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Transaction Date', 'Account Number', 'Transaction Type', 'Amount', 'Description'])
        writer.writerows(cleaned_data)

def separate_transactions(input_file, output_file_individual, output_file_aggregated):
    individual_transactions = []
    aggregated_transactions = []

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Account Number'] == 'YEARLY TOTAL' or row['Account Number'] == 'SUBTOTAL':
                
                aggregated_transactions.append(row)
            else:
                individual_transactions.append(row)
        print

    # Write individual transactions to output file
    with open(output_file_individual, 'w', newline='') as csvfile:
        fieldnames = ['Transaction Date', 'Account Number', 'Transaction Type', 'Amount', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(individual_transactions)

    # Write aggregated transactions to output file
    with open(output_file_aggregated, 'w', newline='') as csvfile:
        fieldnames = ['Transaction Date','Account Number',  'Transaction Type', 'Amount', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(aggregated_transactions)

def reconcile_transactions(individual_transactions, aggregated_transactions):
    # Calculate total amount from individual transactions
    individual_total = sum(float(transaction['Amount']) for transaction in individual_transactions)

    print('individual_total',individual_total)

    # Calculate total amount from aggregated transactions
    aggregated_total = sum(float(transaction['Amount']) for transaction in aggregated_transactions)
    print('aggregated_total',aggregated_total)

    # Reconcile totals
    if individual_total == aggregated_total:
        print("Transaction totals matching")
    else:
        print("Transaction totals not matching")

def detect_anomalies(input_file, output_file, threshold=1.6):
    transactions = []

    with open(input_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            transactions.append(row)

    # Extract amounts from transactions
    amounts = [float(transaction['Amount']) for transaction in transactions]
  

    # Calculate mean and standard deviation of transaction amounts
    mean_amount = np.mean(amounts)
    
    std_amount = np.std(amounts)
 

    # Detect anomalies based on Z-score
    anomalies = []
    for transaction in transactions:
        amount = float(transaction['Amount'])
        z_score = (amount - mean_amount) / std_amount
        if np.abs(z_score) > threshold:
            anomalies.append(transaction)

    # Write anomalies to output file
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Transaction Date', 'Account Number', 'Transaction Type', 'Amount', 'Description']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(anomalies)

    return anomalies

if __name__ == "__main__":

    # provide file path .csv file 
    input_file = r"E:\script\banking_data_assignment.csv"

    # provide output file path
    cleaned_output_file = r"E:\script\cleaned_banking_data.csv"
    individual_output_file = r"E:\script\individual_transactions.csv"
    aggregated_output_file = r"E:\script\aggregated_transactions.csv"
    anomalies_output_file = r"E:\script\anomalies_detected.csv"

    # Data Cleaning
    clean_data(input_file, cleaned_output_file)

    # Data Analysis - Separating Transactions
    separate_transactions(cleaned_output_file, individual_output_file, aggregated_output_file)

    # Data Analysis - Reconciling Transactions
    individual_transactions = []
    with open(individual_output_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        individual_transactions = list(reader)

    aggregated_transactions = []
    with open(aggregated_output_file, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        aggregated_transactions = list(reader)

    reconcile_transactions(individual_transactions, aggregated_transactions)

    # Anomaly Detection
    detected_anomalies = detect_anomalies(individual_output_file, anomalies_output_file)

    if detected_anomalies:
        print(f"{len(detected_anomalies)} anomalies detected")
    else:
        print("No anomalies detected.")
