
import csv
import json
from datetime import datetime

DT_FORMAT = '%Y-%m-%d'


class Entry(object):
    """A container that holds one CSV row. Each CSV row represents one
    investment transaction by one investor.

    Attributes:
        dt (datetime): date field of CSV row
        shares (int): number of shares owned by this investor
        cash_paid (float): how much this investor has invested
        investor (str): name of the investor for this transaction
    """
    def __init__(self, dt, row):
        """Instantiates the entry class with a CSV row that represents an
        investment transaction.

        Args:
            row (list): List of strings for the transaction.
            dt (datetime): datetime for the transaction.
        """
        self.dt = dt
        self.shares = int(row[1])
        self.cash_paid = float(row[2])
        self.investor = row[3]

    def to_ownership(self, total_shares):
        """Maps the values of this class to a dictionary object.

        Args:
            total_shares (int): Total no. of outstanding shares for a co.
        """
        return dict(
            investor=self.investor,
            shares=self.shares,
            cash_paid=self.cash_paid,
            ownership=round(float(self.shares) / total_shares * 100, 2)
        )


class CapTableParser(object):
    """Parses a CSV file and outputs a JSON formatted captable.

    Attributes:
        dt (datetime): The end date of when transactions should be counted.

    Note:
        if dt is set to t=100 transactions happening after t=100 will be
        ignored.
    """
    def __init__(self):
        self.dt = None

    def main(self, csv_path, date_s):
        """Prints a JSON formatted captable from the CSV file.

        Args:
            csv_path (str): file path of the csv file.
            date_s (str): a string in DT_FORMAT for the transaction cut off
                point.
        """
        if date_s:
            self.dt = datetime.strptime(date_s, DT_FORMAT)
        else:
            self.dt = datetime.now()

        cash_raised = 0
        total_number_of_shares = 0
        entries = {}        # 'investor': entry

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)            # skip header line

            for row in csv_reader:
                if not row:             # skip empty lines
                    continue

                dt = datetime.strptime(row[0], DT_FORMAT)
                if dt > self.dt:        # skip entires that happens after dt
                    continue

                # Indiscriminate: all transactions are kosher after this point

                investor = row[3]
                if investor in entries:
                    entry = entries[investor]
                else:
                    entry = Entry(dt, row)
                    entries[investor] = entry

                cash_raised += entry.cash_paid
                total_number_of_shares += entry.shares

        print(json.dumps(dict(
            date=self.dt.strftime(DT_FORMAT),
            cash_raised=cash_raised,
            total_number_of_shares=total_number_of_shares,
            ownership=[
                e.to_ownership(total_number_of_shares) for e in entries.values()
            ],
        )))


if __name__ == "__main__":
    import sys

    ctp = CapTableParser()

    if len(sys.argv) == 2:
        ctp.main(sys.argv[1], None)
    elif len(sys.argv) == 3:
        ctp.main(sys.argv[1], sys.argv[2])
    else:
        print('python captable.py <csv_file_path> [YYYY-MM-DD]')

