import PySimpleGUI as sg
import pandas as pd
import sqlite3
import os

conn_banks = sqlite3.connect(
    r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\databases\all_banks.sqlite')
cur_banks = conn_banks.cursor()

cur_banks.execute('SELECT name FROM BANKS')
bank_names = cur_banks.fetchall()
add_new_bank = 'Add New Bank'
bank_names.append(add_new_bank)

# Add some color to the window
sg.theme('DarkTeal9')

layout = [
    [sg.Text('Please fill out the following fields:')],
    [sg.Text('Bank Name', size=(15, 1)),
     sg.Combo(bank_names, key='bank_name')],
    [sg.Text('Rate', size=(15, 1)), sg.InputText(key='rate')],
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
        date = values['date']
        amount = values['amount']
        rate = values['rate']

        for name in bank_names:
            if name == 'Add New Bank':
                filepath = r'C:\Users\Taimur Adam\Desktop\website test copy\website\data\add_new_bank_form.py'
                os.startfile(filepath)
                break
            else:
                name_of_bank = name_of_bank[0]

            name = name[0]
            if name_of_bank == name:
                path = f'C:\\Users\\Taimur Adam\\Desktop\\website test copy\\website\\data\\databases\\{name}_bank_data.sqlite'
                conn = sqlite3.connect(path)
                cur = conn.cursor()
                cur.execute(
                    'SELECT id FROM DATES WHERE DATES.date = (?)', (date,))
                date_id = cur.fetchone()[0]
                cur.execute(
                    'UPDATE PRINCIPAL SET debit = (?) WHERE date_id = (?)', (amount, date_id,))
                cur.execute(
                    'UPDATE PRINCIPAL SET rate = (?) WHERE date_id = (?)', (rate, date_id,))

                conn.commit()
                conn.close()
