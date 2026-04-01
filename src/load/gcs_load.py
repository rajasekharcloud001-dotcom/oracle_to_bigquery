from google.cloud import storage
from google.cloud import bigquery
from google.cloud import secretmanager
from datetime import datetime
import os

def get_secret(secret_id, project_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def create_table_if_not_exists(project_id, dataset, table):
    """Table లేకపోతే automatically create చేయి"""
    
    client = bigquery.Client(project=project_id)
    table_ref = f"{project_id}.{dataset}.{table}"
    
    try:
        client.get_table(table_ref)
    except:
        schema = [
            bigquery.SchemaField("transaction_id", "STRING"),
            bigquery.SchemaField("account_number", "STRING"),
            bigquery.SchemaField("amount", "FLOAT"),
            bigquery.SchemaField("transaction_type", "STRING"),
            bigquery.SchemaField("txn_date", "DATE"),
            bigquery.SchemaField("status", "STRING"),
            bigquery.SchemaField("bank_name", "STRING"),
        ]
        table_obj = bigquery.Table(table_ref, schema=schema)
        client.create_table(table_obj)

def upload_to_gcs(local_file, project_id):
    """Local file ని GCS కి upload చేయి"""
    
    # Secret Manager నుండి bucket name తీసుకో
    bucket_name = get_secret("bucket-name", project_id)
    
    # GCS client
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    
    # File name
    file_name = os.path.basename(local_file)
    blob = bucket.blob(file_name)
    
    # Upload చేయి
    blob.upload_from_filename(local_file)
    
    gcs_path = f"gs://{bucket_name}/{file_name}"
    
    return gcs_path

if __name__ == "__main__":
    project_id = os.getenv("GCP_PROJECT", "hello-dev-491512")
    dataset = get_secret("dataset-name", project_id)
    table = get_secret("table-name", project_id)
    
    # Table create చేయి (లేకపోతే)
    create_table_if_not_exists(project_id, dataset, table)
    
    # GCS కి upload చేయి
    today = datetime.now().strftime("%Y-%m-%d")
    local_file = f"data/banking_data_{today}.csv"
    upload_to_gcs(local_file, project_id)