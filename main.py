import os
import sys

sys.path.append("src/extract")
sys.path.append("src/load")

from oracle_extract import extract_from_oracle
from gcs_load import upload_to_gcs, create_table_if_not_exists, get_secret
from bigquery_load import load_to_bigquery

from datetime import datetime

def main():
    print("🚀 Banking Pipeline Started!")
    print("=" * 50)
    
    # Project ID తీసుకో
    project_id = os.getenv("GCP_PROJECT", "hello-dev-491512")
    print(f"📌 Project: {project_id}")
    
    # Today's date
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"📅 Date: {today}")
    
    # Step 1: Extract from Oracle
    print("\n📥 Step 1: Extract from Oracle")
    print("-" * 30)
    local_file = extract_from_oracle()
    
    # Step 2: Upload to GCS
    print("\n☁️ Step 2: Upload to GCS")
    print("-" * 30)
    dataset = get_secret("dataset-name", project_id)
    table = get_secret("table-name", project_id)
    create_table_if_not_exists(project_id, dataset, table)
    gcs_path = upload_to_gcs(local_file, project_id)
    
    # Step 3: Load to BigQuery
    print("\n📊 Step 3: Load to BigQuery")
    print("-" * 30)
    load_to_bigquery(gcs_path, project_id)
    
    print("\n" + "=" * 50)
    print("✅ Pipeline Completed Successfully!")
    print(f"📅 Date: {today}")
    print(f"📌 Project: {project_id}")

if __name__ == "__main__":
    print("enter the program")
    main()