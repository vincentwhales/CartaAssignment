import csv
import json
from datetime import datetime

DT_FORMAT = '%Y-%m-%d'


class Transaction(object):
    """Represents one transaction by one investor into this company.

    Attributes:
        dt (datetime): date field of CSV row
        shares (int): number of shares owned by this investor
        cash_paid (float): how much this investor has invested
        investor (str): name of the investor for this transaction
    """
    def __init__(self, row):
        """Instantiates a Transaction instance.

        Args:
            row (list): List of values for the transaction.
        """
        self.dt = datetime.strptime(row[0], DT_FORMAT)
        self.shares = int(row[1])
        self.cash_paid = float(row[2])
        self.investor = row[3]


class Investor(object):
    """A container to hold all transaction for one investor

    Attributes:
        name (str): name of the investor
        shares (int): total number of shares across all transactions
        cash_paid (float): total amt of cash paid by investor across all
            transactions.
    """
    def __init__(self, name):
        self.name = name
        self.shares = 0
        self.cash_paid = 0

    def add_transaction(self, transaction):
        """Adds a transaction to this investor.
        """
        self.shares += transaction.shares
        self.cash_paid += transaction.cash_paid

    def to_ownership(self, total_shares):
        """Maps the values of this instance to a dictionary object.

        Args:
            total_shares (int): Total no. of outstanding shares for a co.
        """
        return dict(
            investor=self.name,
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
        total_shares = 0
        investors = {}        # { name: investor }

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)            # skip header line

            for row in csv_reader:
                if not row:             # skip empty lines
                    continue

                transaction = Transaction(row)
                if transaction.dt > self.dt:    # skip entires that happens after dt
                    continue

                # Indiscriminate: all transactions are kosher after this point

                name = transaction.investor
                if name in investors:
                    investor = investors[name]
                else:
                    investor = Investor(name)
                    investors[name] = investor

                investor.add_transaction(transaction)
                cash_raised += investor.cash_paid
                total_shares += investor.shares

        print(json.dumps(dict(
            date=self.dt.strftime(DT_FORMAT),
            cash_raised=cash_raised,
            total_shares=total_shares,
            ownership=[
                i.to_ownership(total_shares) for i in investors.values()
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
