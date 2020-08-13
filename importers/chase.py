from .autoPayCard import AutoPayCard

from dateutil.parser import parse

from titlecase import titlecase

import csv
import os
import re

class ChaseCCImporter(AutoPayCard):
    def __init__(self, account, lastfour, autoPayAccount, statementCloseDay, paymentDay):
        self.account = account
        self.lastfour = lastfour
        self.autoPayAccount = autoPayAccount
        self.statementCloseDay = statementCloseDay
        self.paymentDay = paymentDay
        self.payments = dict([])

    def identify(self, f):
        return re.match('Chase{}.*\.CSV'.format(self.lastfour), os.path.basename(f.name))

    def getDate(self, row):
        return parse(row['Transaction Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return row['Amount']
    def getCategory(self, row):
        if 'BudgetCategory' in row:
            return row['BudgetCategory']
        return None
    def isPayment(self, row):
        return row['Description'] == "AUTOMATIC PAYMENT - THANK"
