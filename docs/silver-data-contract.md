\# Silver Data Contract



\## Dataset

RRC County Production



\## Grain

One row represents one county, in one district, for one year, one month, and one oil/gas code.



\## Candidate Key

\- COUNTY\_NO

\- DISTRICT\_NO

\- CYCLE\_YEAR

\- CYCLE\_MONTH

\- OIL\_GAS\_CODE



Observed result:

\- Total rows: 242,740

\- Unique candidate keys: 242,740

\- Duplicate candidate key rows: 0



\## Confirmed Expectations



\### Required identifying fields

The following fields must not be null:

\- COUNTY\_NO

\- DISTRICT\_NO

\- CYCLE\_YEAR

\- CYCLE\_MONTH

\- OIL\_GAS\_CODE



\### Month

CYCLE\_MONTH must be between 1 and 12.



\### Candidate key uniqueness

The candidate key must be unique within the dataset.



\## Observed but Not Yet Confirmed as Contract Rules



\### Oil/Gas Code

Observed values:

\- O

\- G



This requires source or domain confirmation before enforcing it as an official rule.



\### Production Volumes

No negative values were observed in:

\- CNTY\_OIL\_PROD\_VOL

\- CNTY\_GAS\_PROD\_VOL

\- CNTY\_COND\_PROD\_VOL

\- CNTY\_CSGD\_PROD\_VOL



A non-negative production rule requires source or domain confirmation before enforcement.



\### Fully Null Source Columns

Twelve source columns were observed as 100% null in the Bronze dataset.



These columns should not be removed from Bronze.

Their treatment in Silver requires an explicit design decision.

