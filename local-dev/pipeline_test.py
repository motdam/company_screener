import json
import logging
from datetime import datetime
from google.cloud import storage, bigquery
import requests
from typing import Any

from config import (
    QUICKFS_API_KEY,
    RAW_BUCKET,
    RAW_PREFIX,
    PROJECT_ID,
    DATASET_ID,
    KEY_METRICS,
    COMPANIES_TABLE,
    FINANCIALS_ANNUAL_TABLE,
    LAST_UPDATE_TABLE
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main pipeline execution"""
    test_symbol = "BABA:US"
    
    try:
        # Fetch data
        data = fetch_quickfs_data(test_symbol)
        
        # Save to GCS
        gcs_path = upload_to_gcs(data, test_symbol)
        logger.info(f"Data saved to GCS: {gcs_path}")
        
        # Load to BigQuery
        load_to_bigquery(data, test_symbol)
        logger.info("Pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}")
        raise

def fetch_quickfs_data(symbol: str):
    """Fetch company data from QuickFS API"""
    url = f"https://public-api.quickfs.net/v1/data/all-data/{symbol}"
    headers = {"X-QFS-API-Key": QUICKFS_API_KEY}
    
    logger.info(f"Fetching data for {symbol}...")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json()["data"]

def upload_to_gcs(data: dict, symbol: str):
    """Upload raw JSON data to GCS"""
    storage_client = storage.Client()
    bucket = storage_client.bucket(RAW_BUCKET)
    
    # Format GCS path
    current_date = datetime.now().strftime("%Y%m%d")
    company_id = symbol.replace(":", "_")
    blob_path = f"{RAW_PREFIX}/{company_id}/{current_date}/data.json"
    
    # Upload data
    blob = bucket.blob(blob_path)
    logger.info(f"Uploading to GCS: {blob_path}")
    blob.upload_from_string(json.dumps(data, indent=2))
    logger.info(f"Successfully uplaoded to GCS: {blob_path}")
    return blob_path

def load_to_bigquery(data: dict, symbol: str):
    """Load data to BigQuery tables"""

    bq_client = bigquery.Client(project=PROJECT_ID)
    
    # Debug prints
    logger.info(f"Client project: {bq_client.project}")
    logger.info(f"Project ID from config: {PROJECT_ID}")
    
    # Companies table  
    table_id = f"`{PROJECT_ID}.{DATASET_ID}.{COMPANIES_TABLE}`"
    logger.info(f"Attempting to use table_id: {table_id}")
    
    # Prepare company data
    company_row = {
        "company_id": symbol,
        "name": data.get("metadata", {}).get("name"),
        "exchange": data.get("metadata", {}).get("exchange"),
        "country": symbol.split(":")[-1] if ":" in symbol else "US",
        "industry": data.get("metadata", {}).get("industry"),
        "sector": data.get("metadata", {}).get("sector"),
        "insert_date": datetime.now().date().isoformat()
    }
    

    financials_rows = []
    annual_data = data["financials"]["annual"]
    for idx, fiscal_year in enumerate(annual_data.get("fiscal_year_number", [])):
        # Format the period date if it's a date object
        
        # Initialize the base row
        row = {
            "company_id": symbol,
            "period_end_date": f"{annual_data["period_end_date"][idx]}-01",
            "fiscal_year": fiscal_year
        }
        
        # Add requested metrics with proper formatting
        for metric in KEY_METRICS:
            if metric in annual_data and len(annual_data[metric]) > idx:
                row[metric] = annual_data[metric][idx]
        
        financials_rows.append(row)
    
    # Insert data
    logger.info("Loading data to BigQuery...")
    
    # Companies table
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{COMPANIES_TABLE}"
    errors = bq_client.insert_rows_json(table_id, [company_row])
    if errors:
        logger.error(f"Error inserting company data: {errors}")
    
    # Financials table
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{FINANCIALS_ANNUAL_TABLE}"
    errors = bq_client.insert_rows_json(table_id, financials_rows)
    if errors:
        logger.error(f"Error inserting financials data: {errors}")
    
    # Update control table
    control_row = {
        "company_id": symbol,
        "last_fiscal_year_processed": financials_rows[-1]["fiscal_year"] if financials_rows else None,
        "last_update_date": datetime.now().date().isoformat()
    }
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{LAST_UPDATE_TABLE}"
    errors = bq_client.insert_rows_json(table_id, [control_row])
    if errors:
        logger.error(f"Error updating control table: {errors}")


if __name__ == "__main__":
    main()