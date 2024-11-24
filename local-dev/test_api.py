from quickfs import QuickFS
import json
from datetime import datetime
import os
from pathlib import Path
import logging

from config import (
    QUICKFS_API_KEY,
    RAW_BUCKET,
    RAW_PREFIX,
    ERROR_PREFIX
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_quickfs_connection():
    """Test connection to QuickFS API using BABA as test case"""
    try:
        # Initialize client
        client = QuickFS(api_key=QUICKFS_API_KEY)
        
        # Test usage endpoint
        usage = client.get_usage()
        logger.info(f"API Quota Usage: {usage}")
        
        # Get BABA data
        logger.info("Fetching BABA data...")
        data = client.get_data_full(symbol="BABA:US")
        
        # Save raw response
        current_date = datetime.now().strftime("%Y%m%d")
        output_dir = Path("data/raw")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_file = output_dir / f"BABA_US_{current_date}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
            
        logger.info(f"Saved raw data to {output_file}")
        
        # Print some basic info
        logger.info(f"Company Name: {data['metadata']['name']}")
        logger.info(f"Exchange: {data['metadata']['exchange']}")
        logger.info(f"Available Fiscal Years: {len(data['financials']['annual'])}")
        
        return data
        
    except Exception as e:
        logger.error(f"Error testing API: {str(e)}")
        raise

if __name__ == "__main__":
    test_quickfs_connection()