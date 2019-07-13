
## Captable.py

A script that parses a transaction csv file to produce a cap table.

## Usage

1. `python captable.py <csv_file_path>`
2. `python captable.py <csv_file_path> -e [date_str]`

- csv_file_path: the location of the transaction csv file
- date_str: optional argument for the cut off transaction date in the format of YYYY-MM-DD.

## Design Decisions

The csv file can have multiple investments from one investor across different date.

Thus, I've created a separate container class "Investor" to sum all the transactions up
up to the end date.

To simplify parsing of the CSV rows, I've created a basic class Transaction to
contain all the logic involved.



