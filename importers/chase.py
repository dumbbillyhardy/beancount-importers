from .autoPayCard import AutoPayCard

from dateutil.parser import parse

from titlecase import titlecase

class ChaseCCImporter(AutoPayCard):
    def getDate(self, row):
        return parse(row['Transaction Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return '-'+row['Amount'] if row['Amount'][0] != '-' else row['Amount'][1:]
    def isPayment(self, row):
        return row['Description'].find("AUTOMATIC PAYMENT - THANK") != -1
