from beancount.core.number import D
from beancount.ingest import importer
from beancount.core import account
from beancount.core import amount
from beancount.core import flags
from beancount.core import data
from beancount.core.position import Cost

import datetime
import calendar
import csv
import os

class AutoPayCard(importer.ImporterProtocol):
    def __init__(self, account, autoPayAccount, statementCloseDay, paymentDay):
        self.account = account
        self.autoPayAccount = autoPayAccount
        self.statementCloseDay = statementCloseDay
        self.paymentDay = paymentDay
        self.payments = dict([])

    def getDate(row):
        pass
    def getDesc(row):
        pass
    def getAmt(row):
        pass
    def getCategory(row):
        pass
    def isPayment(self, row):
        pass

    def extract(self, f):
        entries = []

        with open(f.name) as f:
            for index, row in enumerate(csv.DictReader(f)):
                if self.isPayment(row):
                    continue

                meta = data.new_metadata(f.name, index)

                txn = self.extractRow(row, meta)
                entries.append(txn)
                self.addPaymentFor(txn, self.getDate(row), self.getAmt(row), self.getCategory(row))


        entries.extend(self.payments.values())
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
                "Liabilities:"+trans_category,
                amount.Amount(D(trans_amt), 'USD'),
                None, None, None, None
            ))
        return txn

    def addPaymentFor(self, txn, trans_date, trans_amt, trans_category):
        months_to_add = 1 if trans_date.day > self.statementCloseDay else 0
        payment_date = set_days(add_months(trans_date, months_to_add), self.paymentDay)
        
        paymentTxn = self.payments[payment_date.isoformat()] if payment_date.isoformat() in self.payments else data.Transaction(
                meta=txn.meta,
                date=payment_date,
                flag=flags.FLAG_OKAY,
                payee=self.account + " Payment",
                narration="",
                tags=set(),
                links=set(),
                postings=[])
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


        self.payments[payment_date.isoformat()] = paymentTxn



def preparePayAccount(account, category):
    if category is not None:
        return account+":Month:"+category
    return account

def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year,month)[1])
    return datetime.date(year, month, day)

def set_days(sourcedate, day):
    return datetime.date(sourcedate.year, sourcedate.month, day)
