import os
import sys

sys.path.append("src/extract")
sys.path.append("src/load")

from oracle_extract import extract_from_oracle
from gcs_load import upload_to_gcs, create_table_if_not_exists, get_secret
from bigquery_load import load_to_bigquery

from datetime import datetime

def main():
    print("Banking Pipeline Started!")
    print("=" * 50)
    
    project_id = os.getenv("GCP_PROJECT", "hello-dev-491512")
    print(f"Project: {project_id}")
    
    today = datetime.now().strftime("%Y-%m-%d")
    print(f"Date: {today}")
    
    print("\nStep 1: Extract from Oracle")
    print("-" * 30)
    try:
        local_file = extract_from_oracle()
    except ValueError as e:
        print(f"ERROR: {e}")
        print("No data to process today! Pipeline stopped!")
        sys.exit(0)
    
    print("\nStep 2: Upload to GCS")
    print("-" * 30)
    dataset = get_secret("dataset-name", project_id)
    table = get_secret("table-name", project_id)
    create_table_if_not_exists(project_id, dataset, table)
    gcs_path = upload_to_gcs(local_file, project_id)
    
    print("\nStep 3: Load to BigQuery")
    print("-" * 30)
    load_to_bigquery(gcs_path, project_id)
    
    print("\n" + "=" * 50)
    print("Pipeline Completed Successfully!")
    print(f"Date: {today}")
    print(f"Project: {project_id}")

if __name__ == "__main__":
    main()