import oracledb
import pandas as pd
from datetime import datetime
import os

def extract_from_oracle():
    """get only todays records only"""

    connection = oracledb.connect(
        user="banking_user",
        password="Oracle123#",
        dsn="localhost:1521/XEPDB1"
    )

    today = datetime.now().strftime("%Y-%m-%d")
    
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
    WHERE TRUNC(transaction_date) = TRUNC(SYSDATE)
    """

    df = pd.read_sql(query, connection)

    # Validation
    if len(df) == 0:
        connection.close()
        raise ValueError(f"No data found for {today}! Pipeline stopped!")

    print(f"Extracted {len(df)} records from Oracle")

    connection.close()

    filename = f"data/banking_data_{today}.csv"
    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False)
    
    print(f"Saved to {filename}")
    return filename

if __name__ == "__main__":
    print("extracting the data")
    extract_from_oracle()