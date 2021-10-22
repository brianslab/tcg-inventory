from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys, getopt
from cardListParse import getTcgpCards

# Initialize client
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('tcg-inventory-SA.json', scope)
client = gspread.authorize(creds)

# Iinitialiaze sheets
inv = "MTG Cards"

storage = client.open(inv).worksheet("storage")
trades = client.open(inv).worksheet("trades")
# breena = client.open(inv).worksheet("EDH-Breena")
# nicol = client.open(inv).worksheet("EDH-Nicol Bolas")
# child = client.open(inv).worksheet("EDH-Child of Alara")
# etron = client.open(inv).worksheet("MOD-Eldrazi Tron")

# Parse arguments
addfile = ""
to = "storage"
parseTcgpOrder = False
try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:t:o", ["help", "add=", "to=", "order"])
except:
    print("ERROR: invalid arguments. See -h or --help")
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-h", "--help"):
        print("-add : adds cards from file")
        sys.exit()
    elif opt in ("-a", "--add"):
        addfile = arg
    elif opt in ("-t", "--to"):
        to = client.open(inv).worksheet(arg)
    elif opt in ("-o", "--order"):
        parseTcgpOrder = True

if addfile:
    if parseTcgpOrder:
        print("adding cards from TCGPlayer order", addfile, "to", to)
        additions = getTcgpCards(addfile)
    else:
        print("adding cards from", addfile, "to", to)

item = 0
for item in range(0, len(additions[0])):
    to.append_row([additions[0][item], additions[1][item]])