from beancount.core.number import D
from beancount.ingest import importer
from beancount.core import account
from beancount.core import amount
from beancount.core import flags
from beancount.core import data
from beancount.core.position import Cost

from dateutil.parser import parse

from titlecase import titlecase

import csv
import os
import re

class PncImporter(importer.ImporterProtocol):
    def __init__(self, account, filePattern):
        self.account = account
        self.filePattern = filePattern

    def identify(self, f):
        return re.match(self.filePattern + '.*\.csv', os.path.basename(f.name))

    def extract(self, f):
        entries = []

        with open(f.name) as f:
            for index, row in enumerate(csv.DictReader(f)):
                trans_date = parse(row['Date']).date()
                trans_desc = titlecase(row['Description'])
                withdrawal = row['Withdrawals'][1:]
                deposit = row['Deposits'][1:]
                trans_amt = deposit if deposit else '-'+withdrawal

                if trans_desc.find("ONLINE CREDIT CARD PMT") != -1:
                    # Record these at the bank level
                    continue

                meta = data.new_metadata(f.name, index)

                txn = data.Transaction(
                    meta=meta,
                    date=trans_date,
                    flag=flags.FLAG_OKAY,
                    payee=trans_desc,
                    narration="",
                    tags=set(),
                    links=set(),
                    postings=[],
                )

                txn.postings.append(
                    data.Posting(
                        self.account,
                        amount.Amount(D(trans_amt), 'USD'),
                        None, None, None, None
                    )
                )

                entries.append(txn)

        return entries
