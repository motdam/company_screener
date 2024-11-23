# Company Screener

Prototype/development version !

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

## Disclaimer

This software is for educational and research purposes only. Nothing in this project may be construed as financial, legal or tax advice. The content is solely for learning about data pipelines and financial metrics.

This is not an offer to buy or sell financial instruments. Never invest more than you can afford to lose. You should consult a registered professional advisor before making any investment.

The author is not affiliated with or promoting QuickFS services. The code connects to QuickFS API but users must obtain their own API key and comply with QuickFS terms of service.

Historical financial data may be incomplete or inaccurate. No warranty is made about the accuracy of data or suitability for any purpose.
