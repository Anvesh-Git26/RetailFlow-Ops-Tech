import pandas as pd
import numpy as np
import datetime

def generate_retail_data():
    # 1. Product Master Data (Retail Ops Focus)
    products = pd.DataFrame({
        'product_id': range(101, 111),
        'product_name': ['Milk', 'Bread', 'Eggs', 'Rice', 'Oil', 'Sugar', 'Soap', 'Flour', 'Tea', 'Coffee'],
        'unit_price': [60, 45, 120, 800, 150, 50, 35, 300, 250, 450],
        'unit_cost': [50, 35, 100, 700, 130, 40, 25, 250, 200, 380],
        'lead_time_days': [2, 1, 2, 5, 4, 3, 7, 5, 6, 6] 
    })

    # 2. Transactions Data (Analytics Focus)
    # Generates 2000 random sales over the last year
    dates = pd.date_range(start='2025-01-01', end='2025-12-31', freq='H')
    data_size = 2000
    
    transactions = pd.DataFrame({
        'transaction_id': range(1000, 1000 + data_size),
        'timestamp': np.random.choice(dates, data_size),
        'customer_id': np.random.randint(5000, 5200, data_size), 
        'product_id': np.random.choice(products['product_id'], data_size),
        'quantity': np.random.randint(1, 5, data_size)
    })

    # 3. Inventory Data (Operational Mastery Focus)
    inventory = pd.DataFrame({
        'product_id': products['product_id'],
        'current_stock': np.random.randint(5, 100, 10)
    })

    # Save to CSV
    transactions.to_csv('transactions.csv', index=False)
    products.to_csv('products.csv', index=False)
    inventory.to_csv('inventory.csv', index=False)
    print("✅ Files Generated: transactions.csv, products.csv, inventory.csv")

if __name__ == "__main__":
    generate_retail_data()