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

def removeWhitespace(str):
    return str.replace(" ", "")

class YnabImporter(importer.ImporterProtocol):
    def __init__(self, account_mapping):
        self.account_mapping = account_mapping

    def identify(self, f):
        if not re.match('Billy.*Register\.csv', os.path.basename(f.name)):
            return False

        return True

    def extract(self, f):
        entries = []

        with open(f.name) as f:
            for index, row in enumerate(csv.DictReader(f)):
                account = removeWhitespace(row['\ufeffAccount'])

                date = parse(row['Date']).date()
                desc = titlecase(row['Payee'])
                inflow = row['Outflow'][1:]
                outflow = row['Inflow'][1:]
                amt = amount.Amount(D('-'+inflow if inflow != '0.00' else outflow), 'USD')

                group = removeWhitespace(row['Category Group'])
                category = removeWhitespace(row['Category'])

                if desc.find("Transfer : ") != -1 and account != self.main_account:
                    # Let other accounts handle transfers.
                    to_account = removeWhitespace(desc[11:].replace("Transfer : ", ""))
                elif group == "Inflow":
                    to_account = "Equity:Opening-Balances"
                else: 
                    to_account = "Expenses:"+group+":"+category

                meta = data.new_metadata(f.name, index)

                txn = data.Transaction(
                    meta=meta,
                    date=date,
                    flag=flags.FLAG_OKAY,
                    payee=desc,
                    narration="",
                    tags=set(),
                    links=set(),
                    postings=[],
                )

                txn = data.Transaction(
                    meta, date, flags.FLAG_OKAY, None, desc, data.EMPTY_SET, data.EMPTY_SET, [
                        data.Posting(account, amt, None, None, None, None),
                        data.Posting(to_account, -amt, None, None, None, None),
                    ])

                entries.append(txn)

        return entries
