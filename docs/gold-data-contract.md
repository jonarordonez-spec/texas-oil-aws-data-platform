
# Gold Data Contract

## Dataset
county_oil_production_annual

## Purpose
Provide annual county-level oil production
aggregations for analytics and econometric research.

## Source
Silver dataset:
data/silver/county_production/county_production.parquet

## Output
data/gold/county_oil_production_annual.parquet

## Grain
One row per COUNTY_NO and CYCLE_YEAR.

## Schema

| Column | Logical type | Description |
|---|---|---|
| COUNTY_NO | Integer | County identifier |
| CYCLE_YEAR | Integer | Reporting year |
| annual_oil_production | Integer | Sum of reported oil production |
| months_reported | Integer | Number of distinct reported months |
| has_12_months | Boolean | True when 12 distinct months are recorded |

## Transformation Rules
1. Filter OIL_GAS_CODE = "O".
2. Group by COUNTY_NO and CYCLE_YEAR.
3. Sum CNTY_OIL_PROD_VOL.
4. Count distinct CYCLE_MONTH values.
5. Set has_12_months = (months_reported == 12).

## Quality Rules
- County-year keys must not be null.
- County-year keys must be unique.
- Annual production must not be null.
- Annual production must be non-negative.
- months_reported must be between 1 and 12.
- has_12_months must match months_reported == 12.
- Zero production values must be preserved.

## Known Limitations
- Partial-year observations are retained.
- Twelve reported months do not guarantee complete
  or accurate source reporting.
- The 2026 data currently has substantial
  partial-year coverage.
- Production units require source verification.
- Aggregation across districts requires
  confirmation of source reporting semantics.

## Current Local Validation
- Gold rows: 7,865.
- Gold columns: 5.
- Duplicate county-year keys: 0.
- Twelve-month coverage: 7,594 rows.
- Partial monthly coverage: 271 rows.
