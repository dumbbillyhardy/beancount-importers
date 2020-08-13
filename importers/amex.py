from beancount.core.number import D
from beancount.ingest import importer
from beancount.core import account
from beancount.core import amount
from beancount.core import flags
from beancount.core import data
from beancount.core.position import Cost

from dateutil.parser import parse
import datetime
import calendar

from titlecase import titlecase

import csv
import os
import re

class AmexImporter(importer.ImporterProtocol):
    def __init__(self, account, autoPayAccount, statementCloseDay, paymentDay):
        self.account = account
        self.autoPayAccount = autoPayAccount
        self.statementCloseDay = statementCloseDay
        self.paymentDay = paymentDay

    def identify(self, f):
        if not re.match('amex.*\.csv', os.path.basename(f.name)):
            return False

        return True

    def extract(self, f):
        entries = []
        payments = dict([])

        with open(f.name) as f:
            for index, row in enumerate(csv.DictReader(f)):
                trans_date = parse(row['Date']).date()
                trans_desc = titlecase(row['Description'])
                trans_amt  = row['Amount']
                trans_category = row['BudgetCategory'] if 'BudgetCategory' in row else ''

                if trans_desc == "Online Payment - Thank You":
                    # Assume we always pay off everything
                    continue

                if trans_desc == "Payment Received - Thank You":
                    # Assume we always pay off everything
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
                    postings=[
                        data.Posting(
                            self.account,
                            amount.Amount(-1*D(trans_amt), 'USD'),
                            None, None, None, None
                        ),
                        data.Posting(
                            "Liabilities:"+trans_category,
                            amount.Amount(D(trans_amt), 'USD'),
                            None, None, None, None
                        )
                    ],
                )

                entries.append(txn)

                months_to_add = 1 if trans_date.day > self.statementCloseDay else 0
                payment_date = set_days(add_months(trans_date, months_to_add), self.paymentDay)
                
                paymentTxn = payments[payment_date.isoformat()] if payment_date.isoformat() in payments else data.Transaction(
                        meta=meta,
                        date=payment_date,
                        flag=flags.FLAG_OKAY,
                        payee="Payment of "+trans_desc,
                        narration="",
                        tags=set(),
                        links=set(),
                        postings=[]
                    )
                paymentTxn.postings.extend([
                    data.Posting(self.account,
                        amount.Amount(D(trans_amt), 'USD'), 
                        None, None, None, None
                    ),
                    data.Posting(preparePayAccount(self.autoPayAccount, trans_category),
                        amount.Amount(-1*D(trans_amt), 'USD'),
                        None, None, None, None
                    ),
                ])

                payments[payment_date.isoformat()] = paymentTxn

        entries.extend(payments.values())
        return entries

def preparePayAccount(account, category):
    return account+":Month:"+category

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def set_days(sourcedate, day):
    return datetime.date(sourcedate.year, sourcedate.month, day)
