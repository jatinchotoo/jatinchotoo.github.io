import pandas as pd
import os
import random
from datetime import datetime, timedelta

def generate_sovereign_ledger():
    # 1. Ensure directory structure
    os.makedirs('data', exist_ok=True)
    
    # 2. Configuration
    output_path = 'data/ESFE_FACT_GL.csv'
    columns = ['txn_date', 'account_code', 'account_name', 'debit', 'credit', 'entity', 'description']
    
    accounts = [
        ('1000', 'Cash'),
        ('1200', 'Accounts Receivable'),
        ('2000', 'Accounts Payable'),
        ('4000', 'Revenue'),
        ('5000', 'Cost of Goods Sold'),
        ('6000', 'Operating Expenses')
    ]
    
    entities = ['Equinox Corp', 'Sovereign Ltd']
    data = []
    start_date = datetime(2025, 1, 1)

    # 3. Generate 50 rows of deterministic IFRS-style data
    for i in range(50):
        # Generate random date within a 90-day window
        date_obj = start_date + timedelta(days=random.randint(0, 90))
        txn_date = date_obj.strftime('%Y-%m-%d')
        
        acc_code, acc_name = random.choice(accounts)
        entity = random.choice(entities)
        amount = round(random.uniform(100.00, 5000.00), 2)
        
        # Ensure either Debit or Credit is populated, never both
        if random.choice([True, False]):
            debit = amount
            credit = 0.0
        else:
            debit = 0.0
            credit = amount
            
        data.append([
            txn_date, 
            acc_code, 
            acc_name, 
            debit, 
            credit, 
            entity, 
            f"General entry for {acc_name}"
        ])

    # 4. Create DataFrame and write to CSV
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(output_path, index=False)
    
    print(f"File created: {output_path}")

if __name__ == "__main__":
    generate_sovereign_ledger()
    