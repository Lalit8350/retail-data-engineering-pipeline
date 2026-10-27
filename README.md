# Retail Data Engineering Pipeline

## Project Overview

This project builds a data-cleaning and analytics pipeline using the Online Retail dataset. It uses Python and pandas to clean transaction data, perform data-quality checks, and prepare the processed data for analysis in PostgreSQL.

The goal is to demonstrate practical data engineering skills, including data cleaning, validation, relational database loading, and analytical SQL.

## Tech Stack

- **Language:** Python
- **Data processing:** pandas
- **Database:** PostgreSQL
- **Query language:** SQL
- **Testing:** Python data-quality tests

## Dataset

The project uses the UCI Online Retail dataset, containing transactions from a UK-based online retailer between December 2010 and December 2011.

Source: https://archive.ics.uci.edu/dataset/352/online+retail

## Project Structure

```text
retail-data-engineering-pipeline/
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── inspect_data.py
│   └── clean_data.py
├── sql/
│   └── retail_analysis.sql
├── tests/
│   └── test_clean_data.py
├── notebooks/
└── README.md
```

## Data Processing

The original dataset contained 541,909 rows. After removing 5,268 exact duplicate rows, the processed dataset contained 536,641 rows.

The cleaning process includes:

- Inspecting the source data and identifying missing values.
- Removing exact duplicate records.
- Cleaning text fields and handling missing values.
- Converting customer IDs to a nullable integer type.
- Creating flags for cancellations and data-quality issues.
- Calculating `LineAmount` as quantity multiplied by unit price.
- Saving the processed data as a CSV file.
- Running automated data-quality tests.

## SQL Analysis

PostgreSQL is used to analyse the processed transaction data.

The SQL analysis includes:

1. Transaction amounts by country.
2. Monthly transaction summaries.
3. Top products by transaction amount.
4. Investigation of large manual cancellation records.
5. Top merchandise product by country using CTEs and window functions.

## Data Investigation Findings

### Cancellation Investigation

The product `PAPER CRAFT, LITTLE BIRDIE` had a transaction of 80,995 units worth £168,469.60 and a corresponding cancellation of -80,995 units worth -£168,469.60.

The two records offset each other, producing a net quantity and net line amount of zero for those records.

### Manual Adjustments

The analysis identified 31 manual cancellation records with absolute line amounts greater than £1,000. Their combined absolute amount was £106,760.41.

These records were flagged for further investigation rather than automatically classified as data errors.

## Current Project Status

Completed:

- Source-data inspection.
- Python data cleaning.
- Data-quality validation tests.
- PostgreSQL database and table setup.
- Loading the processed CSV into PostgreSQL.
- SQL aggregation, ranking, and cancellation investigations.

Planned improvements:

- Improve repeatable database-loading and validation steps.
- Expand automated data-quality tests.
- Add pipeline logging and error handling.
- Explore orchestration and cloud data engineering tools.

## Key Learning Outcomes

This project demonstrates practical experience with Python data processing, PostgreSQL, SQL aggregations, CTEs, window functions, data-quality validation, and transaction-level investigation.
