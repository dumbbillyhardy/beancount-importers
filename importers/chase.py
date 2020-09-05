from .autoPayCard import AutoPayCard

from dateutil.parser import parse

from titlecase import titlecase

class ChaseCCImporter(AutoPayCard):
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
