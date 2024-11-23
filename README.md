# company_screener
Prototype financial data pipeline to screen companies using QuickFS fundamental data - focusing on annual reports and basic screening metrics

A lightweight data pipeline that:
- Fetches fundamental financial data from QuickFS API
- Stores raw data in GCS and processed data in BigQuery
- Runs configurable screening criteria to identify companies matching investment criteria
- Generates monthly screening reports

Built with:
- Python
- Google Cloud (BigQuery, Cloud Storage, Cloud Functions)
- QuickFS API

Currently focused on:
- Annual report data
- Basic financial screening metrics (ROIC, margins, etc.)
- US market companies



