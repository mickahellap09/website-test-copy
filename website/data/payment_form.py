import PySimpleGUI as sg
import sqlite3
import update_databases

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM banks')
bank_names = cur_banks.fetchall()

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)), sg.Combo(bank_names, key='bank_name')],
    [sg.Text('Payment type', size=(15, 1)), sg.Checkbox(
        'Principal', key='principal'), sg.Checkbox('Markup', key='markup')],
    [sg.Text('Amount', size=(15, 1)), sg.InputText(key='amount')],
    [sg.Text('Date DD/MM/YYYY', size=(15, 1)), sg.InputText(key='date')],
    [sg.Submit(), sg.Exit()]
]

window = sg.Window('Borrowing Form', layout)


while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Submit':
        name_of_bank = values['bank_name']
        name_of_bank = name_of_bank[0]
        date = values['date']
        amount = values['amount']
        amount = float(amount)
        amount = -abs(amount)
        debit_or_credit = 'credit'

        if values['principal'] == True:
            transaction_type = 'principal'
        elif values['markup'] == True:
            transaction_type = 'markup'
        else:
            break
        
        update_databases.add_new_transaction_payment(name_of_bank, transaction_type, debit_or_credit, amount, date)
