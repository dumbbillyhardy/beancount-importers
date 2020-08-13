from .autoPayCard import AutoPayCard
from dateutil.parser import parse

from titlecase import titlecase

import re
import os

class AmexImporter(AutoPayCard):
    def identify(self, f):
        if not re.match('amex.*\.csv', os.path.basename(f.name)):
            return False

        return True

    def getDate(self, row):
        return parse(row['Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return row['Amount']
    def getCategory(self, row):
        if 'BudgetCategory' in row:
            return row['BudgetCategory']
        return None
    def isPayment(self, row):
        return row['Description'] == "Online Payment - Thank You" or  row['Description'] == "Payment Received - Thank You"
