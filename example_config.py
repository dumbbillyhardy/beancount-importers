import os, sys

# beancount doesn't run from this directory
sys.path.append(os.path.dirname(__file__))

# importers located in the importers directory
from importers import amex, chase, pnc, ynab

CONFIG = [
    chase.ChaseCCImporter('Liabilities:US:Chase:Sapphire', 'XXXX'),
    amex.AmexImporter('Liabilities:US:Amex:RoseGold'),
    pnc.PncImporter('Assets:US:PNC:Checking', 'accountActivity'),
    ynab.YnabImporter({}),
]
