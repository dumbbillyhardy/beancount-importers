from .baseAccount import BaseAccount

from dateutil.parser import parse

from titlecase import titlecase

class DiscoverImporter(BaseAccount):
    def getDate(self, row):
        return parse(row['Trans. Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return row['Amount']
    def isPayment(self, row):
        return row['Description'].find('DIRECTPAY FULL BALANCE') != -1
