import oracledb
import pandas as pd
from datetime import datetime
import os


def extract_from_oracle():
    """get only todays records only"""
    print("extracting from oracle db")

    #oracle connections

    connection = oracledb.connect(
        user="banking_user",
        password="Oracle123#",
        dsn="localhost:1521/XEPDB1"
    )

    print("connected to oracle db")

    # todays date

    today = datetime.now().strftime("%Y-%m-%d")
    
    #query -  todays records to extract

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

    # dataframe
    df = pd.read_sql(query,connection)

    print(f"Exctracted {len(df)} records from oracle")

    #close the connections
    connection.close()

    #convert into a csv

    filename = f"data/banking_data_{today}.csv"
    os.makedirs("data", exist_ok=True)
    df.to_csv(filename, index=False)

    print(f"✅ Saved to {filename}")
    return filename

if __name__ == "__main__":
    print("extracting the data")
    extract_from_oracle()
