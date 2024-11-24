from datetime import datetime
import os
from pathlib import Path

# Set Credentials

# Get root project directory (2 levels up from config.py)
PROJECT_ROOT = Path(__file__).parent.parent

# Paths
SECRETS_DIR = PROJECT_ROOT / "secrets"
CREDENTIALS_PATH = SECRETS_DIR / "company_screener_dev_sa.json"
QUICKFS_KEY_PATH = SECRETS_DIR / "quickfs_key.txt"

# Set GCP credentials env variable
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = str(CREDENTIALS_PATH)

# Read QuickFS key from file
def get_quickfs_key():
    with open(QUICKFS_KEY_PATH) as f:
        return f.read().strip()  # Just reads the raw key

# API Settings
QUICKFS_API_KEY = get_quickfs_key()


# GCP Settings
PROJECT_ID = "company-screener-dev"
DATASET_ID = "datawarehouse_dev"
LOCATION = "europe-west2"  # BigQuery dataset location

# GCS Settings 
RAW_BUCKET = f"company-screener-datalake-dev"
RAW_PREFIX = "raw/annual"
ERROR_PREFIX = "errors"
REPORTS_PREFIX = "reports"

# BigQuery Table Names
COMPANIES_TABLE = "companies"
# FINANCIALS_ANNUAL_TABLE = "financials_annual"
# LAST_UPDATE_TABLE = "company_last_update"
SCREENING_RESULTS_TABLE = "screening_results"

# TEMP VALUES FOR TESTING
FINANCIALS_ANNUAL_TABLE = "financials_annual_temp"
LAST_UPDATE_TABLE = "company_last_update_temp"

# Initial list of metrics we care about for basic screening
KEY_METRICS = [
    'revenue',
    'operating_income',
    'net_income',
    'fcf',
    'roic',
    'operating_margin',
    'total_assets',
    'total_equity',
    'total_debt'
]

# Date settings
CURRENT_DATE = datetime.now().strftime('%Y-%m-%d')