
import csv
import json
from datetime import datetime

FORMAT = '%Y-%m-%d'


class Entry(object):
    def __init__(self, row):
        self.dt = datetime.strptime(row[0], FORMAT)
        self.shares = int(row[1])
        self.cash_paid = float(row[2])
        self.investor = row[3]

    def to_ownership(self, total_shares):
        return dict(
            investor=self.investor,
            shares=self.shares,
            cash_paid=self.cash_paid,
            ownership=round(float(self.shares) / total_shares * 100, 2)
        )


class CapTableParser(object):

    def __init__(self):
        self.dt = None

    def main(self, csv_path, date_s):
        if date_s:
            self.dt = datetime.strptime(date_s, FORMAT)
        else:
            self.dt = datetime.now()

        cash_raised = 0
        total_number_of_shares = 0
        entries = []

        with open(csv_path, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)            # skip header line

            for row in csv_reader:
                if not row:             # skip empty lines
                    continue

                entry = Entry(row)
                if entry.dt > self.dt:  # skip entires that happens AFTER
                    continue

                cash_raised += entry.cash_paid
                total_number_of_shares += entry.shares
                entries.append(entry)

        print(json.dumps(dict(
            date=self.dt.strftime(FORMAT),
            cash_raised=cash_raised,
            total_number_of_shares=total_number_of_shares,
            ownership=[
                e.to_ownership(total_number_of_shares) for e in entries
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
        print('python captable.py <CSV file path> [YYYY-MM-DD]')

