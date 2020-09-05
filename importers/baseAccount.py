from beancount.core.number import D
from beancount.core import amount
from beancount.core import data
from beancount.core import flags
from beancount.ingest import importer

import csv
import os
import re

class BaseAccount(importer.ImporterProtocol):
    def __init__(self, filePattern, account):
        self.filePattern = filePattern
        self.account = account

    def identify(self, f):
        return re.match(self.filePattern, os.path.basename(f.name))

    def getDate(row):
        pass
    def getDesc(row):
        pass
    def getAmt(row):
        pass
    def getCategory(row):
        pass

    def extract(self, f):
        entries = []

        with open(f.name) as f:
            for index, row in enumerate(csv.DictReader(f)):
                meta = data.new_metadata(f.name, index)

                txn = self.extractRow(row, meta)
                entries.append(txn)

        return entries

    def extractRow(self, row, meta):
        trans_date = self.getDate(row)
        trans_desc = self.getDesc(row)
        trans_amt  = self.getAmt(row)
        trans_category = self.getCategory(row)

        txn = data.Transaction(
            meta=meta,
            date=trans_date,
            flag=flags.FLAG_OKAY,
            payee=trans_desc,
            narration="",
            tags=set(),
            links=set(),
            postings=[
                data.Posting(
                    self.account,
                    amount.Amount(-1*D(trans_amt), 'USD'),
                    None, None, None, None
                ),
            ],
        )
        if trans_category is not None:
            txn.postings.append(data.Posting(
                "Expenses:"+trans_category,
                amount.Amount(D(trans_amt), 'USD'),
                None, None, None, None
            ))
        return txn

