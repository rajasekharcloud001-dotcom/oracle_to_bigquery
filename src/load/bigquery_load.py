from google.cloud import bigquery
from google.cloud import secretmanager
from datetime import datetime
import os

def get_secret(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def load_to_bigquery(gcs_path, project_id):
    
    print("Loading to BigQuery...")
    
    dataset = get_secret("dataset-name", project_id)
    table = get_secret("table-name", project_id)
    
    client = bigquery.Client(project=project_id)
    
    table_ref = f"{project_id}.{dataset}.{table}"
    
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        write_disposition="WRITE_APPEND",
        schema=[
            bigquery.SchemaField("transaction_id", "STRING"),
            bigquery.SchemaField("account_number", "STRING"),
            bigquery.SchemaField("amount", "FLOAT"),
            bigquery.SchemaField("transaction_type", "STRING"),
            bigquery.SchemaField("txn_date", "DATE"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("bank_name", "STRING"),
        ]
    )
    
    load_job = client.load_table_from_uri(
        gcs_path, table_ref, job_config=job_config
    )
    load_job.result()
    
    print(f"Loaded to {table_ref}")

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT", "hello-dev-491512")
    today = datetime.now().strftime("%Y-%m-%d")
    gcs_path = f"gs://banking-data-dev-491512/banking_data_{today}.csv"
    load_to_bigquery(gcs_path, project_id)