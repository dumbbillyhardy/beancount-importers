from .autoPayCard import AutoPayCard

from dateutil.parser import parse

from titlecase import titlecase

import os
import re

class DiscoverImporter(AutoPayCard):
    def identify(self, f):
        return re.match('Discover-.*\.csv', os.path.basename(f.name))

    def getDate(self, row):
        return parse(row['Trans. Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return row['Amount']
    def getCategory(self, row):
        if 'BudgetCategory' in row:
            return row['BudgetCategory']
        return None
    def isPayment(self, row):
        return row['Description'].find('DIRECTPAY FULL BALANCE') != -1
