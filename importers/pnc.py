from .baseAccount import BaseAccount

from dateutil.parser import parse

from titlecase import titlecase

class CashBuilderImporter(BaseAccount):
    def getDate(self, row):
        return parse(row['Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        return '-'+row['Amount'][2:] if row['Amount'][0] == '-' else row['Amount'][1:]
    def isPayment(self, row):
        return row['Description'].find("ONLINE CREDIT CARD PMT") != -1


class VirtualWalletImporter(BaseAccount):
    def skip(self, row):
        if 'Skip' in row and row['Skip'] == 'true':
            return True
        pncCat = row['Category']
        return pncCat == "Paychecks" or pncCat == "Credit Card Payments"
    def getDate(self, row):
        return parse(row['Date']).date()
    def getDesc(self, row):
        return titlecase(row['Description'])
    def getAmt(self, row):
        withdrawal = row['Withdrawals'][1:]
        deposit = row['Deposits'][1:]
        return '-'+deposit if deposit else withdrawal
