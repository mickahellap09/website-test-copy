import PySimpleGUI as sg
import pandas as pd
import sqlite3

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM BANKS')
bank_names = cur_banks.fetchall()

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)), sg.Combo(bank_names, key='bankName')],
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
        -abs(amount)

        for name in bank_names:
            name = name[0]
            if name_of_bank == name:
                path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{name.upper()}_bank_data.sqlite'
                conn = sqlite3.connect(path)
                cur = conn.cursor()

                cur.execute(
                    'SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
                date_id = cur.fetchone()[0]
                if values['principal'] == True:
                    cur.execute(
                        'UPDATE PRINCIPAL SET credit = (?) WHERE date_id = (?)', (amount, date_id,))
                else:
                    cur.execute(
                        'UPDATE MARKUP SET credit = (?) WHERE date_id = (?)', (amount, date_id,))

                conn.commit()
                conn.close()
