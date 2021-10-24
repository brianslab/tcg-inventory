from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys, getopt
import time
from cardListParse import getTcgpCards, getDecklistCards

# Initialize client
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('tcg-inventory-SA.json', scope)
client = gspread.authorize(creds)

# Iinitialiaze inventory
inv = client.open("MTG Cards")

# Parse arguments
addfile = ""
to = inv.worksheet("storage")
parseTcgpOrder = False
parseDecklist = False

try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:t:pln:d:s:", ["help", "add=", "to=", "tcgp", "list", "new=", "delete=", "shoplist="])
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
        to = inv.worksheet(arg)
    elif opt in ("-p", "--tcgp"):
        parseTcgpOrder = True
    elif opt in ("-l", "--list"):
        parseDecklist = True
    elif opt in ("-n", "--new"):
        try:
            inv.worksheet(arg)
            print("Existing deck:", arg)
        except:
            print("Creating deck:", arg)
            newSheet = inv.add_worksheet(title=arg, rows="1000", cols="2")
        finally:
            to = inv.worksheet(arg)
    elif opt in ("-d", "--delete"):
        delete = inv.worksheet(arg)
        print("Deleting deck:", delete.title)
        addfile = delete.title
        additions = [delete.col_values(1), delete.col_values(2)]
        inv.del_worksheet(delete)
    elif opt in ("-s", "--shoplist"):
        print("Checking inventory for cards in", arg)
        desiredList = getDecklistCards(arg)
        ownedCards = inv.worksheet("storage")
        shoppingList = list(set(desiredList[0]).difference(ownedCards.col_values(1)))
        shopFile = arg + ".shop"
        print("Saving shopping list to", shopFile)
        with open(shopFile, "w") as f:
            for item in shoppingList:
                f.write(item + '\n')
        f.close()


if addfile:
    if parseTcgpOrder:
        print("adding cards from TCGPlayer order", addfile, "to", to.title)
        additions = getTcgpCards(addfile)
    elif parseDecklist:
        print("adding cards from decklist", addfile, "to", to.title)
        additions = getDecklistCards(addfile)
    else:
        print("adding cards from", addfile, "to", to.title)
    item = 0
    for item in range(0, len(additions[0])):
        to.append_row([additions[0][item], additions[1][item]])
        time.sleep(1)