#!/usr/bin/python3

from oauth2client.service_account import ServiceAccountCredentials
import gspread
import sys, getopt

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
breena = client.open(inv).worksheet("EDH-Breena")
nicol = client.open(inv).worksheet("EDH-Nicol Bolas")
child = client.open(inv).worksheet("EDH-Child of Alara")
etron = client.open(inv).worksheet("MOD-Eldrazi Tron")

# Parse arguments
addfile = ""
to = storage.title
try:
    opts, args = getopt.getopt(sys.argv[1:], "ha:t:", ["add=", "to="])
except:
    print("ERROR: invalid arguments. See -h")
    sys.exit(2)
for opt, arg in opts:
    if opt == "-h":
        print("-add : adds cards from file")
        sys.exit()
    elif opt in ("-a", "--add"):
        addfile = arg
    elif opt in ("-t", "--to"):
        to = arg

print("adding cards from", addfile, "to", to)