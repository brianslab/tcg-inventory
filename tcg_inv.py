from oauth2client.service_account import ServiceAccountCredentials
import gspread

scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
creds = ServiceAccountCredentials.from_json_keyfile_name('tcg-inventory-SA.json', scope)
client = gspread.authorize(creds)

storage = client.open("MTG Cards").worksheet("storage")
breena = client.open("MTG Cards").worksheet("EDH-Breena")

storage.update_cell(1,3, "Hello World!")
breena.update_cell(1,3, "Hello World!")