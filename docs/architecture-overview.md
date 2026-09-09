# Texas Oil AWS Data Platform

## Project Goal

Build a cloud-based data engineering platform for Texas oil production data using AWS.

The project remains independent from the original `texas-oil-analytics` repository.

## Architecture

```text
Texas Railroad Commission Source
        |
        v
Landing / Raw
- Original source files
- Immutable / as-is
- Source format (.dsv)
        |
        v
Bronze
- Source-aligned
- Queryable
- Parquet
- Basic structural validation
- Minimal transformation
        |
        v
Silver
- Validated against the Silver data contract
- Required identifiers are not null
- CYCLE_MONTH is between 1 and 12
- Candidate key is unique
- Reliable granular data
        |
        v
Gold
- Analysis-ready datasets
- Aggregations
- Econometrics
- Machine learning features
- Business and analytical outputs
```

## Current Implemented Flow

### Landing / Raw

The original RRC county production file is preserved in its source format.

### Bronze

The raw `.dsv` source file is read, minimally validated, and written as Parquet.

Current dataset:

`data/bronze/county_production/county_production.parquet`

### Silver

The Bronze dataset is validated against the initial Silver data contract before being written to Silver.

Current validation rules:

- Required identifying fields must not be null.
- `CYCLE_MONTH` must be between 1 and 12.
- The candidate key must be unique.

Candidate key:

- `COUNTY_NO`
- `DISTRICT_NO`
- `CYCLE_YEAR`
- `CYCLE_MONTH`
- `OIL_GAS_CODE`

Current dataset:

`data/silver/county_production/county_production.parquet`

## Automated Testing

Silver validation behavior is tested with `pytest`.

Current tests verify that:

- Invalid months are rejected.
- Null identifiers are rejected.
- Duplicate candidate keys are rejected.
- Valid data is accepted.

## Current Focus

- Medallion layer responsibilities
- Data quality
- Parquet
- Reproducible Python pipelines
- Automated testing
- Git and GitHub workflow
- AWS integration

## Future Components

- Upload pipeline outputs to Amazon S3
- AWS Glue
- Amazon Athena
- Data layout and partitioning
- Additional Silver transformations
- Gold datasets
- Automated data quality
- Orchestration
- Monitoring and observability
- CI/CD
