from .autoPayCard import AutoPayCard
from dateutil.parser import parse

from titlecase import titlecase

import re

class AmexImporter(AutoPayCard):
    def getDate(self, row):
        return parse(row['Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return row['Amount']
    def isPayment(self, row):
        return row['Description'].find('AUTOPAY PAYMENT - THANK YOU') != -1
