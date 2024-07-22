import csv
import gspread
import time
import regex as re
import os

VALID_DATE = re.compile('[0,1]?[0-9]/[0-3]?[0-9]/[2020-2029]')

VALID_MONTH = {'JANUARY' : '2024-01',
               'FEBRUARY': '2024-02',
               'MARCH': '2024-03',
               'APRIL': '2024-04',
               'MAY': '2024-05',
               'JUNE': '2024-06',
               'JULY': '2024-07',
               'AUGUST': '2024-08',
               'SEPTEMBER': '2024-09',
               'OCTOBER': '2024-10',
               'NOVEMBER': '2024-11',
               'DECEMBER': '2024-12'}

CATEGORIES = {'AUTOMATIC WITHDRAWAL, APPLECARD GSBANK PAYMENT WEB (S)' : 'APPLE CARD',
              'AUTOMATIC WITHDRAWAL, BEST BUY AUTO PYMT WEB (R)': 'BEST BUY',
              'AUTOMATIC WITHDRAWAL, DISCOVER E-PAYMENT WEB (S)' : 'DISCOVER',
              'AUTOMATIC DEPOSIT, SPICY THAI RESTADIRECT DEP PPD': 'Salary',
              'Gasoline': 'Gas',
              'Restaurants': 'Food',
              'Grocery': 'Food',
              'Travel/ Entertainment': 'Entertainment',
              'Supermarkets': 'Food',
              'Spotify USA': 'Subscriptions',
              'GOOGLE*Google': 'Subscriptions',
              'Apple Services': 'Subscriptions',
              'AUDIBLE*RX87W1I61 AMZN.COM/BILLNJ3ULB3X91K7N': 'Subscriptions',
              'MOBILE BANKING FUNDS TRANSFER TO LOAN NUMBER 1': 'Rent & Bills'
              }




def template_statement(file, date_idx, name_idx, debit_idx, credit_idx, categ_idx, TRANSACTIONS, credit_multiplier= 1):
    file = PATH +'/' + file

    with open(file, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            if VALID_DATE.match(row[0]):
                date = row[date_idx]
                name = row[name_idx]
                amount = float(row[debit_idx]) * credit_multiplier if row[debit_idx] not in ['','0'] else float(row[credit_idx])
                category = row[categ_idx] if categ_idx else CATEGORIES.get(name, 'other')
                if category in CATEGORIES:
                    category = CATEGORIES[category]
                if name in CATEGORIES:
                    category = CATEGORIES[name]
                transaction = ((date, name, amount, category))
                TRANSACTIONS.append(transaction)



if __name__ == '__main__':
    total_trans = []

    # Get User Prompts for Which Month
    while True:
        TIME = input("What month are you banking for? ").upper()
        if TIME in VALID_MONTH:
            break
        print("Incorrect input")

    # Path to File
    PATH = f"C:/Users/ChangeMe/Desktop/Folder_of_CSV/{TIME}"
    try:
        files = os.listdir(PATH)
        for file in files:
            if file.startswith('afcu'):
                template_statement(file, 0, 2, 3, 4, None, total_trans)
            if file.startswith('apple'):
                template_statement(file, 0, 3, 6, None, 4, total_trans, -1)
            if file.startswith('disc'):
                template_statement(file, 0, 2, 3, None, 4, total_trans, -1)
            if file.startswith('ssfcu_check'):
                template_statement(file, 0, 2, 3, 4, None, total_trans, -1)
            if file.startswith('ssfcu_save'):
                template_statement(file, 0, 1, 2, 3, None, total_trans, -1)

        total_trans.sort()
        sa = gspread.service_account()
        sh = sa.open("Bank Spreadsheet")

        worksheet = sh.worksheet(f'{VALID_MONTH[TIME]}')

        for row in total_trans:
            worksheet.insert_row([row[0], row[1], row[3], row[2]], 7)
            time.sleep(2)

    except:
        print("No File Directory Found")



