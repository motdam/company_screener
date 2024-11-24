-- project_id & dataset need to be set up prior to run (run did manually in bq console)

DROP TABLE IF EXISTS company-screener-dev.datawarehouse_dev.companies;
CREATE TABLE company-screener-dev.datawarehouse_dev.companies (
    company_id STRING,
    name STRING,
    exchange STRING,
    country STRING,
    industry STRING,
    sector STRING,
    insert_date DATE
);


DROP TABLE IF EXISTS company-screener-dev.datawarehouse_dev.financials_annual;
CREATE TABLE company-screener-dev.datawarehouse_dev.financials_annual (
    company_id STRING,
    period_end_date DATE,
    fiscal_year INT64,
    revenue FLOAT64,
    operating_income FLOAT64,
    net_income FLOAT64,
    fcf FLOAT64,
    roic FLOAT64,
    operating_margin FLOAT64,
    total_assets FLOAT64,
    total_equity FLOAT64,
    total_debt FLOAT64
)
;

DROP TABLE IF EXISTS company-screener-dev.datawarehouse_dev.company_last_update;
CREATE TABLE company-screener-dev.datawarehouse_dev.company_last_update (
    company_id STRING,
    last_fiscal_year_processed INT64,
    last_update_date DATE
);