import oracledb
import pandas as pd
from datetime import datetime, timedelta
import os

def extract_from_oracle():
    """get only yesterday's records"""
    
    connection = oracledb.connect(
        user="banking_user",
        password="Oracle123#",
        dsn="localhost:1521/XEPDB1"
    )

    # Use YESTERDAY's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    query = """
        SELECT 
            transaction_id,
            account_number,
            amount,
            transaction_type,
            TO_CHAR(transaction_date, 'YYYY-MM-DD') as txn_date,
            status,
            bank_name
        FROM banking_transactions
        WHERE TRUNC(transaction_date) = TRUNC(SYSDATE - 1)
    """

    df = pd.read_sql(query, connection)

    # Validation
    if len(df) == 0:
        connection.close()
        raise ValueError(f"No data found for {yesterday}! Pipeline stopped!")

    print(f"Extracted {len(df)} records from Oracle for {yesterday}")

    connection.close()

    filename = f"data/banking_data_{yesterday}.csv"
    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False)
    
    print(f"Saved to {filename}")
    return filename

if __name__ == "__main__":
    print("extracting yesterday's data")
    extract_from_oracle()